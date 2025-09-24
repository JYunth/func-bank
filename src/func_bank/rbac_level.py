from .jwt_decode import decode_jwt
from .exceptions import ValidationError, AuthenticationError
import logging
import time

logger = logging.getLogger(__name__)

def verify_role_level(token: str, min_level: int, secret: str) -> bool:
    """
    Verifies if the JWT token contains a role level greater than or equal to the minimum level.

    Args:
        token (str): The JWT token to verify.
        min_level (int): The minimum required level.
        secret (str): The secret key for decoding the token.

    Returns:
        bool: True if the level is sufficient, False otherwise.
    """
    logger.info("Starting role level verification", extra={"min_level": min_level})
    start_time = time.time()
    if not isinstance(min_level, int):
        logger.error("Invalid min_level type")
        return False
    try:
        payload = decode_jwt(token, secret)
        if payload is None:
            duration = time.time() - start_time
            logger.warning("Role level verification failed: token invalid or expired", extra={"duration": duration})
            return False
        level = payload.get('level')
        if not isinstance(level, int):
            duration = time.time() - start_time
            logger.error("Role level verification failed: invalid level", extra={"duration": duration, "level": level})
            return False
        result = level >= min_level
        duration = time.time() - start_time
        logger.info("Role level verification completed", extra={"duration": duration, "result": result})
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Role level verification failed: unexpected error", extra={"duration": duration, "error": str(e)})
        return False