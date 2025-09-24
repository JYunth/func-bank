from sqlalchemy import MetaData, Table, delete, update
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
        with get_session() as session:
            # Inspect table
            metadata = MetaData()
            table_obj = Table(table, metadata, autoload_with=engine)
            
            # Check if record exists
            columns = [col.name for col in table_obj.columns]
            if 'deleted_at' in columns:
                # Soft delete
                stmt = update(table_obj).where(table_obj.c.id == id).values(deleted_at=datetime.datetime.utcnow())
                result = session.execute(stmt)
                session.commit()
                success = result.rowcount > 0
                duration = time.time() - start_time
                logger.info("Record deleted successfully", extra={"table": table, "id": id, "duration": duration, "soft_delete": True, "deleted": success})
                return success
            else:
                # Hard delete
                stmt = delete(table_obj).where(table_obj.c.id == id)
                result = session.execute(stmt)
                session.commit()
                success = result.rowcount > 0
                duration = time.time() - start_time
                logger.info("Record deleted successfully", extra={"table": table, "id": id, "duration": duration, "soft_delete": False, "deleted": success})
                return success
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during delete", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during delete: {str(e)}")
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during delete", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table: {str(e)}")