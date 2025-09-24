from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import ValidationError, DatabaseError
import logging
import time
from .db_connection import engine, get_session

logger = logging.getLogger(__name__)

def read_record(table: str, id: int) -> dict | None:
    """
    Reads a record from the specified table by its primary key ID.

    Inspects the table schema at runtime.

    Args:
        table (str): The name of the table to read from.
        id (int): The primary key ID of the record to read.

    Returns:
        dict | None: A dictionary of the record's data, or None if not found.

    Raises:
        ValidationError: If the table does not exist or ID is invalid.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting record read", extra={"table": table, "id": id})
    start_time = time.time()
    try:
        with get_session() as session:
            metadata = MetaData()
            table_obj = Table(table, metadata, autoload_with=engine)
            
            stmt = select(table_obj).where(table_obj.c.id == id)
            result = session.execute(stmt).fetchone()
            duration = time.time() - start_time
            if result:
                logger.info("Record read successfully", extra={"table": table, "id": id, "found": True, "duration": duration})
                return dict(result._mapping)
            logger.info("Record not found", extra={"table": table, "id": id, "found": False, "duration": duration})
            return None
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during read", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during read: {str(e)}")
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during read", extra={"table": table, "id": id, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table or ID: {str(e)}")