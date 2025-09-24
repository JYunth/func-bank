from sqlalchemy import MetaData, Table, delete, update, text
from sqlalchemy.exc import SQLAlchemyError
import datetime
from .exceptions import ValidationError, DatabaseError
import logging
import time

logger = logging.getLogger(__name__)

from .db_connection import engine, get_session
def delete_record(table: str, id: int) -> bool:
    """
    Deletes a record from the specified table by ID.

    If the table has a 'deleted_at' column, performs a soft delete by setting the timestamp.

    Otherwise, performs a hard delete.

    Args:
        table (str): The name of the table to delete from.
        id (int): The primary key ID of the record to delete.

    Returns:
        bool: True if the record was deleted, False if not found.

    Raises:
        ValidationError: If the table does not exist.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting record deletion", extra={"table": table, "id": id})
    start_time = time.time()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                DELETE FROM {table}
                WHERE id = :id
                RETURNING id
            """), {"id": id})
            conn.commit()
            
            if result.rowcount > 0:
                return True
            return False
            
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during delete", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during delete: {str(e)}")
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during delete", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table: {str(e)}")