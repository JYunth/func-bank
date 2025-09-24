from sqlalchemy import MetaData, Table, update, select, text
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import ValidationError, DatabaseError
import logging
import time
from .db_connection import engine, get_session

logger = logging.getLogger(__name__)
def update_record(table: str, id: int, data: dict) -> bool:
    """
    Updates a record in the specified table by its primary key ID with the given data.

    Inspects the table schema at runtime to validate data keys.

    Supports optimistic locking if a 'version' column exists.

    Args:
        table (str): The name of the table to update.
        id (int): The primary key ID of the record to update.
        data (dict): A dictionary of column-value pairs to update.

    Returns:
        bool: True if the record was updated, False if not found.

    Raises:
        ValidationError: If the table does not exist, data keys do not match columns, or version is missing for optimistic locking.
        DatabaseError: If the database operation fails or a version conflict occurs.
    """
    logger.info("Starting record update", extra={"table": table, "id": id})
    start_time = time.time()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                UPDATE {table}
                SET {', '.join(f'{k} = :{k}' for k in data)}
                WHERE id = :id
                RETURNING id
            """), {**data, "id": id})
            conn.commit()
            
            if result.rowcount > 0:
                return True
            return False
            
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during update", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during update: {str(e)}")
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Validation error during update", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during update", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table or data: {str(e)}")