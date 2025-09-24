from sqlalchemy import MetaData, Table, insert
from sqlalchemy.exc import SQLAlchemyError
import json
from .exceptions import ValidationError, DatabaseError
import logging
import time

logger = logging.getLogger(__name__)

from .db_connection import engine, get_session

def store_file(filename: str, data: bytes, metadata: dict = {}) -> str:
    """
    Stores a file in the database with associated metadata.

    Validates that the file size does not exceed 10MB.

    Args:
        filename (str): The name of the file.
        data (bytes): The binary data of the file.
        metadata (dict): Optional metadata dictionary to store with the file.

    Returns:
        str: The unique file ID (primary key) as a string.

    Raises:
        ValidationError: If the file size exceeds 10MB or data is invalid.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting file storage", extra={"filename": filename})
    start_time = time.time()
    # Check size limit
    max_size = 10 * 1024 * 1024  # 10MB
    if len(data) > max_size:
        duration = time.time() - start_time
        logger.error("File size exceeds limit", extra={"filename": filename, "duration": duration, "size": len(data)})
        raise ValidationError("File size exceeds 10MB limit")

    try:
        with get_session() as session:
            metadata_obj = MetaData()
            table_obj = Table('files', metadata_obj, autoload_with=engine)

            # Prepare data
            insert_data = {
                'filename': filename,
                'data': data,
                'metadata': json.dumps(metadata)
            }

            # Insert
            stmt = insert(table_obj).values(**insert_data)
            result = session.execute(stmt)
            session.commit()

            # Get the inserted primary key
            if result.inserted_primary_key:
                duration = time.time() - start_time
                logger.info("File stored successfully", extra={"filename": filename, "id": str(result.inserted_primary_key[0]), "duration": duration, "size": len(data)})
                return str(result.inserted_primary_key[0])
            else:
                raise DatabaseError("No primary key returned")
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during store", extra={"filename": filename, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during store: {str(e)}")
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Validation error during store", extra={"filename": filename, "duration": duration, "error": str(e)}, exc_info=True)
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during store", extra={"filename": filename, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid data: {str(e)}")