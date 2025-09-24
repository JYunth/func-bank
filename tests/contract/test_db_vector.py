import pytest
from sqlalchemy import text
from func_bank.db_vector import vector_search
from func_bank.db_connection import engine

# Add embedding column as JSONB for testing
with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE test_table 
        ADD COLUMN IF NOT EXISTS embedding JSONB
    """))
    conn.commit()

    # Insert test data with embeddings
    conn.execute(text("""
        UPDATE test_table
        SET embedding = :embedding
        WHERE id = 1
    """), {"embedding": '[0.1,0.1,0.1]'})
    conn.commit()

def test_vector_search_success():
    # This test will fail until implementation
    table = "test_table"
    embedding = [0.1] * 384  # Assuming 384-dimensional embedding
    limit = 10
    result = vector_search(table, embedding, limit)
    assert isinstance(result, list)
    assert len(result) <= limit
    if result:
        assert isinstance(result[0], dict)

def test_vector_search_no_matches():
    # This test will fail until implementation
    table = "test_table"
    embedding = [1.0] * 384  # Dissimilar embedding
    result = vector_search(table, embedding)
    assert result == []

def test_vector_search_invalid_column():
    with pytest.raises(Exception):  # Well-documented error
        vector_search("test_table", [0.1] * 384, embedding_column="invalid_column")