import jwt
from datetime import datetime, timedelta, timezone
from .exceptions import ValidationError
import logging
import time

logger = logging.getLogger(__name__)

from typing import Any

def encode_jwt(payload: Any, secret: Any, expires_hours: int = 24) -> str:
    """
    Encodes a JWT token with the given payload and secret, adding an expiration time.

    Args:
        payload (dict): The payload data to encode in the token.
        secret (str): The secret key to sign the token.
        expires_hours (int): The number of hours until the token expires. Defaults to 24.

    Returns:
        str: The encoded JWT token string.

    Raises:
        ValidationError: If the payload is not a dictionary or the secret is not a string.
    """
    logger.info("Starting JWT encode")
    start_time = time.time()
    if not isinstance(payload, dict):
        logger.error("Invalid payload type for JWT encode")
        raise ValidationError("Payload must be a dictionary")
    if not isinstance(secret, str):
        logger.error("Invalid secret type for JWT encode")
        raise ValidationError("Secret must be a string")

    payload_with_exp = payload.copy()
    if 'exp' not in payload_with_exp:
        expiration = int((datetime.now(timezone.utc) + timedelta(hours=expires_hours)).timestamp())
        payload_with_exp['exp'] = expiration

    token = jwt.encode(payload_with_exp, secret, algorithm='HS256')
    duration = time.time() - start_time
    logger.info("JWT encoded successfully", extra={"duration": duration, "expires_hours": expires_hours})
    return token