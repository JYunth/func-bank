import pytest
from func_bank.db_create import create_record
from func_bank.db_read import read_record
from func_bank.db_update import update_record
from func_bank.db_delete import delete_record


def test_crud_operations():
    """Integration test for full CRUD cycle: create, read, update, read, delete, verify deletion."""
    table = "users"
    initial_data = {"name": "John", "email": "john@example.com"}

    # Create a record
    record_id = create_record(table, initial_data)
    assert isinstance(record_id, int)

    # Read the record
    record = read_record(table, record_id)
    assert record is not None
    assert record["name"] == "John"
    assert record["email"] == "john@example.com"

    # Update the record
    update_data = {"name": "Jane"}
    update_success = update_record(table, record_id, update_data)
    assert update_success is True

    # Read the record again to verify update
    updated_record = read_record(table, record_id)
    assert updated_record is not None
    assert updated_record["name"] == "Jane"
    assert updated_record["email"] == "john@example.com"  # unchanged

    # Delete the record
    delete_success = delete_record(table, record_id)
    assert delete_success is True

    # Verify deletion
    deleted_record = read_record(table, record_id)
    assert deleted_record is None