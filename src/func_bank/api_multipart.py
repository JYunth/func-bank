import logging
import time
from typing import Any
from .exceptions import ValidationError

logger = logging.getLogger(__name__)

def handle_multipart(request: Any) -> dict:
    """
    Parses a multipart request to extract files and form data.

Validates that the total file size does not exceed 1MB.

Args:
    request: The multipart request object containing files and form data.

Returns:
    dict: A dictionary with 'files' and 'data' keys, or empty dict if no data.

Raises:
    ValidationError: If the total file size exceeds the 1MB limit.
"""
    logger.info("Starting multipart handling")
    start_time = time.time()
    try:
        files = request.files
        data = request.form

        # Check size limits: assume 1MB total for files
        total_size = sum(len(content) for content in files.values())
        if total_size > 1000000:
            raise ValidationError("Total file size exceeds 1MB limit")

        if not files and not data:
            duration = time.time() - start_time
            logger.info("Multipart handling completed", extra={"duration": duration, "files_count": 0, "data_keys": []})
            return {}

        duration = time.time() - start_time
        logger.info("Multipart handling completed", extra={"duration": duration, "files_count": len(files), "data_keys": list(data.keys())})
        return {"files": files, "data": data}
    except ValidationError as e:
        duration = time.time() - start_time
        logger.error("Multipart handling failed", extra={"duration": duration, "error": str(e)}, exc_info=True)
        raise
