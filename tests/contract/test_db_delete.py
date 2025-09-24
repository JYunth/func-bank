import pytest
from sqlalchemy import text
from func_bank.db_delete import delete_record
from func_bank.db_connection import engine

def test_delete_record_success():
    # Create test record first
    with engine.connect() as conn:
        result = conn.execute(text(
            "INSERT INTO test_table (name, value) VALUES ('test_delete', 100) RETURNING id"
        ))
        test_id = result.scalar_one()
        conn.commit()
    
    # Now try to delete it
    table = "test_table"
    result = delete_record(table, test_id)
    assert result is True

def test_delete_record_not_found():
    result = delete_record("test_table", 999)
    assert result is False

def test_delete_record_invalid_table():
    with pytest.raises(Exception):
        delete_record("nonexistent_table", 1)