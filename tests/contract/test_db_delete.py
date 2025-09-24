import pytest
from func_bank.db_delete import delete_record

def test_delete_record_success():
    # This test will fail until implementation
    table = "test_table"
    id = 1  # Assuming a record exists
    result = delete_record(table, id)
    assert result is True

def test_delete_record_not_found():
    result = delete_record("test_table", 999)
    assert result is False

def test_delete_record_invalid_table():
    with pytest.raises(Exception):
        delete_record("nonexistent_table", 1)