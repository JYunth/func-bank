from typing import Optional
from .db_create import create_record
from .db_read import read_record
from .db_update import update_record
from .db_delete import delete_record
from .db_query import query_records
from .rbac_verify import verify_role
from .exceptions import (
    ValidationError,
    DatabaseError,
    AuthenticationError,
    AuthorizationError,
)
import logging
import time

logger = logging.getLogger(__name__)


def handle_crud(
    method: str,
    table: str,
    data: Optional[dict] = None,
    id: Optional[int] = None,
    token: Optional[str] = None,
    secret: Optional[str] = None,
    required_role: Optional[str] = None,
) -> dict:
    """
    Handles CRUD operations for the given table based on the HTTP method.

    Args:
        method (str): The HTTP method ('GET', 'POST', 'PUT', 'DELETE').
        table (str): The name of the table to operate on.
        data (Optional[dict]): The data for POST or PUT operations.
        id (Optional[int]): The record ID for GET, PUT, DELETE operations.
        token (Optional[str]): JWT token for authentication.
        secret (Optional[str]): Secret for JWT verification.
        required_role (Optional[str]): Required role for authorization.

    Returns:
        dict: Response dictionary with 'status' and 'data' keys.

    Raises:
        ValidationError: If method is invalid or required data is missing.
        AuthorizationError: If authentication or authorization fails.
    """
    logger.info(
        "Starting CRUD operation",
        extra={
            "method": method,
            "table": table,
            "id": id,
            "required_role": required_role,
        },
    )
    start_time = time.time()
    # Validate method
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise ValidationError(f"Invalid method: {method}")
    try:
        # Auth check if required
        if token and secret and required_role:
            if not verify_role(token, required_role, secret):
                logger.warning(
                    "Access denied for CRUD operation",
                    extra={
                        "method": method,
                        "table": table,
                        "id": id,
                        "required_role": required_role,
                    },
                )
                raise AuthorizationError("Access denied: insufficient permissions")
        if method == "POST":
            if data is None:
                raise ValidationError("Data required for POST")
            record_id = create_record(table, data)
            duration = time.time() - start_time
            logger.info(
                "CRUD operation successful",
                extra={
                    "method": method,
                    "table": table,
                    "id": id,
                    "duration": duration,
                    "record_id": record_id,
                },
            )
            return {"status": "success", "data": record_id}
        elif method == "GET":
            if id is not None:
                record = read_record(table, id)
                duration = time.time() - start_time
                logger.info(
                    "CRUD operation successful",
                    extra={
                        "method": method,
                        "table": table,
                        "id": id,
                        "duration": duration,
                    },
                )
                return {"status": "success", "data": record}
            else:
                records = query_records(table, data or {})
                duration = time.time() - start_time
                logger.info(
                    "CRUD operation successful",
                    extra={
                        "method": method,
                        "table": table,
                        "duration": duration,
                        "records_count": len(records),
                    },
                )
                return {"status": "success", "data": records}
        elif method == "PUT":
            if data is None or id is None:
                raise ValidationError("Data and ID required for PUT")
            success = update_record(table, id, data)
            duration = time.time() - start_time
            logger.info(
                "CRUD operation successful",
                extra={
                    "method": method,
                    "table": table,
                    "id": id,
                    "duration": duration,
                    "updated": success,
                },
            )
            return {"status": "success", "data": success}
        elif method == "DELETE":
            if id is None:
                raise ValidationError("ID required for DELETE")
            success = delete_record(table, id)
            duration = time.time() - start_time
            logger.info(
                "CRUD operation successful",
                extra={
                    "method": method,
                    "table": table,
                    "id": id,
                    "duration": duration,
                    "deleted": success,
                },
            )
            return {"status": "success", "data": success}
    except (ValidationError, AuthorizationError):
        # Re-raise validation and auth errors
        raise
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "CRUD operation failed",
            extra={
                "method": method,
                "table": table,
                "id": id,
                "duration": duration,
                "error": str(e),
            },
            exc_info=True,
        )
        return {"status": "error", "message": str(e)}
