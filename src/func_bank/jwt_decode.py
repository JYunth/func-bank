import jwt
from .exceptions import AuthenticationError
import logging
import time

logger = logging.getLogger(__name__)


def decode_jwt(token: str, secret: str) -> dict | None:
    """
    Decode a JWT token.

    Returns None if token is expired or invalid.
    """
    logger.info("Starting JWT decode")
    start_time = time.time()
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        duration = time.time() - start_time
        logger.info("JWT decoded successfully", extra={"duration": duration})
        return payload
    except jwt.ExpiredSignatureError:
        duration = time.time() - start_time
        logger.warning(
            "JWT decode failed: expired signature", extra={"duration": duration}
        )
        return None
    except jwt.InvalidTokenError:
        duration = time.time() - start_time
        logger.error("JWT decode failed: invalid or malformed token", extra={"duration": duration})
        raise AuthenticationError("Invalid or malformed token")
    except Exception as e:
        duration = time.time() - start_time
        logger.error("JWT decode failed", extra={"duration": duration, "error": str(e)})
        raise AuthenticationError("Failed to decode token")
