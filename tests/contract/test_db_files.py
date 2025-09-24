import pytest
from sqlalchemy import text
from func_bank.db_files import store_file
from func_bank.db_connection import engine

# Create files table if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            data BYTEA NOT NULL,
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
    """))
    conn.commit()

def test_store_file_success():
    # This test will fail until implementation
    filename = "test_file.txt"
    data = b"Hello, world!"
    metadata = {"type": "text"}
    result = store_file(filename, data, metadata)
    assert isinstance(result, str)
    assert len(result) > 0  # Unique file ID

def test_store_file_large_file_error():
    # Assuming large file is > 10MB
    large_data = b"x" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    with pytest.raises(Exception):  # Well-documented error for large files
        store_file("large_file.txt", large_data)