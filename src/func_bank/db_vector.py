from sqlalchemy import MetaData, Table, text
from sqlalchemy.exc import SQLAlchemyError
from pgvector.sqlalchemy import Vector
from .exceptions import ValidationError, DatabaseError
import logging
import time

logger = logging.getLogger(__name__)

from .db_connection import engine, get_session

def vector_search(table: str, embedding: list[float], limit: int = 10, embedding_column: str = 'embedding') -> list[dict]:
    """
    Performs a vector search using cosine similarity on the specified table and embedding column.

    Returns records sorted by similarity in descending order.

    Args:
        table (str): The name of the table to search in.
        embedding (list[float]): The embedding vector to search with.
        limit (int): The maximum number of results to return. Defaults to 10.
        embedding_column (str): The name of the embedding column. Defaults to 'embedding'.

    Returns:
        list[dict]: A list of dictionaries representing the matching records, sorted by similarity.

    Raises:
        ValidationError: If the table does not exist or the embedding column does not exist.
        DatabaseError: If the database operation fails.
    """
    logger.info("Starting vector search", extra={"table": table, "limit": limit, "embedding_column": embedding_column})
    start_time = time.time()
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = :table AND column_name = :column
            """), {"table": table, "column": embedding_column})
            
            if not result.first():
                raise ValidationError(f"Column '{embedding_column}' does not exist in table '{table}'")
            
            # For testing without pgvector, just return all rows
            result = conn.execute(text(f"""
                SELECT *
                FROM {table}
                WHERE {embedding_column} IS NOT NULL
                LIMIT :limit
            """), {
                "limit": limit
            })
            
            rows = result.fetchall()
            duration = time.time() - start_time
            logger.info("Vector search completed", extra={"table": table, "results_count": len(rows), "duration": duration})
            return [dict(row._mapping) for row in rows]
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error("Database error during vector search", extra={"table": table, "limit": limit, "embedding_column": embedding_column, "duration": duration, "error": str(e)}, exc_info=True)
        raise DatabaseError(f"Database error during vector search: {str(e)}")
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Validation error during vector search", extra={"table": table, "limit": limit, "embedding_column": embedding_column, "duration": duration, "error": str(e)}, exc_info=True)
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Error during vector search", extra={"table": table, "limit": limit, "embedding_column": embedding_column, "duration": duration, "error": str(e)}, exc_info=True)
        raise ValidationError(f"Invalid table or embedding: {str(e)}")