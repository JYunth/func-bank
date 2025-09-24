from sqlalchemy import MetaData, Table, select
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import ValidationError, DatabaseError
import logging
import time

logger = logging.getLogger(__name__)

from .db_connection import engine, get_session

def query_records(table: str, filters: dict, limit: int = 100) -> list[dict]:
    """
    Queries records from the specified table with optional filters and limit.

    Inspects the table schema at runtime to validate filters.

    Args:
        table (str): The name of the table to query.
        filters (dict): A dictionary of column-value pairs to filter by.
        limit (int): The maximum number of records to return. Defaults to 100.

    Returns:
        list[dict]: A list of dictionaries representing the matching records.

    Raises:
        ValidationError: If the table does not exist or filter columns do not exist.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting record query", extra={"table": table, "filters": filters, "limit": limit})
    start_time = time.time()
    try:
        with get_session() as session:
            # Inspect table
            metadata = MetaData()
            table_obj = Table(table, metadata, autoload_with=engine)
            
            # Build select
            stmt = select(table_obj)
            
            # Apply filters
            for column, value in filters.items():
                if column in [col.name for col in table_obj.columns]:
                    stmt = stmt.where(table_obj.c[column] == value)
                else:
                    raise ValidationError(f"Filter column '{column}' does not exist in table")
            
            # Apply limit
            stmt = stmt.limit(limit)
            
            # Execute
            result = session.execute(stmt).fetchall()
            duration = time.time() - start_time
            logger.info("Records queried successfully", extra={"table": table, "count": len(result), "duration": duration})
            return [dict(row._mapping) for row in result]
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during query", extra={"table": table, "filters": filters, "limit": limit, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during query: {str(e)}")
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Validation error during query", extra={"table": table, "filters": filters, "limit": limit, "duration": duration, "error": str(e)}, exc_info=True)
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during query", extra={"table": table, "filters": filters, "limit": limit, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table or filters: {str(e)}")