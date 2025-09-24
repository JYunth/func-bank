import pytest
from func_bank.db_read import read_record

def test_read_record_success():
    table = "test_table"
    id = 1
    result = read_record(table, id)
    assert isinstance(result, dict) or result is None

def test_read_record_not_found():
    result = read_record("test_table", 999)
    assert result is None

def test_read_record_invalid_table():
    with pytest.raises(Exception):
        read_record("nonexistent_table", 1)