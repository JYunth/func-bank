from sqlalchemy import create_engine, MetaData, Table, insert, text
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import ValidationError, DatabaseError
import logging
import time
from .db_connection import engine, get_session

logger = logging.getLogger(__name__)

def create_record(table: str, data: dict) -> int:
    """
    Creates a new record in the specified table with the given data.

    The function inspects the table schema at runtime to validate data keys.

    Args:
        table (str): The name of the table to insert into.
        data (dict): A dictionary of column-value pairs to insert.

    Returns:
        int: The primary key ID of the newly created record.

    Raises:
        ValidationError: If the table does not exist or data keys do not match table columns.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting record creation", extra={"table": table})
    start_time = time.time()
    try:
        with get_session() as session:
            # Inspect table
            metadata = MetaData()
            table_obj = Table(table, metadata, autoload_with=engine)
            
            # Check data keys match columns
            columns = [col.name for col in table_obj.columns]
            if not all(key in columns for key in data.keys()):
                raise ValidationError(f"Data keys do not match table columns: {columns}")
            
            # Insert
            stmt = insert(table_obj).values(**data)
            result = session.execute(stmt)
            session.commit()
            if result.inserted_primary_key:
                duration = time.time() - start_time
                logger.info("Record created successfully", extra={"table": table, "id": int(result.inserted_primary_key[0]), "duration": duration})
                return int(result.inserted_primary_key[0])
            else:
                raise DatabaseError("No primary key returned")
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during create", extra={"table": table, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during create: {str(e)}")
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Validation error during create", extra={"table": table, "duration": duration, "error": str(e)}, exc_info=True)
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during create", extra={"table": table, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table or data: {str(e)}")