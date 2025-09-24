from .jwt_decode import decode_jwt
from .exceptions import ValidationError, AuthenticationError
import logging
import time

logger = logging.getLogger(__name__)

def verify_role(token: str, required_role: str, secret: str) -> bool:
    """
    Verifies if the JWT token contains the required role.

    Args:
        token (str): The JWT token to verify.
        required_role (str): The role that must be present in the token.
        secret (str): The secret key for decoding the token.

    Returns:
        bool: True if the role matches, False otherwise.
    """
    logger.info("Starting role verification", extra={"required_role": required_role})
    start_time = time.time()
    try:
        payload = decode_jwt(token, secret)
        if payload is None:
            duration = time.time() - start_time
            logger.warning("Role verification failed: token invalid or expired", extra={"duration": duration})
            return False
        role = payload.get("role")
        if role is None:
            duration = time.time() - start_time
            logger.error("Role verification failed: no role in token", extra={"duration": duration})
            return False
        result = role == required_role
        duration = time.time() - start_time
        logger.info("Role verification completed", extra={"duration": duration, "result": result})
        return result
    except Exception as e:
        duration = time.time() - start_time
        logger.error("Role verification failed: unexpected error", extra={"duration": duration, "error": str(e)})
        return False