from sqlalchemy import create_engine, MetaData, Table, update
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
        with get_session() as session:
            # Inspect table
            metadata = MetaData()
            table_obj = Table(table, metadata, autoload_with=engine)
            
            # Check data keys match columns
            columns = [col.name for col in table_obj.columns]
            if not all(key in columns for key in data.keys()):
                raise ValidationError(f"Data keys do not match table columns: {columns}")
            
            # Prepare update statement
            stmt = update(table_obj).where(table_obj.c.id == id)
            
            # Handle optimistic locking if version column exists
            if 'version' in columns:
                if 'version' not in data:
                    raise ValidationError("Version required for optimistic locking")
                stmt = stmt.where(table_obj.c.version == data['version'])
                # Update all data except version
                update_data = {k: v for k, v in data.items() if k != 'version'}
                stmt = stmt.values(**update_data)
            else:
                stmt = stmt.values(**data)
            
            # Execute update
            result = session.execute(stmt)
            session.commit()
            
            duration = time.time() - start_time
            if result.rowcount > 0:
                logger.info("Record updated successfully", extra={"table": table, "id": id, "duration": duration})
                return True
            else:
                # If version exists and no rows updated, it's a conflict
                if 'version' in columns:
                    logger.warning("Version conflict during update", extra={"table": table, "id": id, "duration": duration})
                    raise DatabaseError("Version conflict: record has been modified")
                else:
                    logger.info("Record not found for update", extra={"table": table, "id": id, "duration": duration})
                    return False  # Not found
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