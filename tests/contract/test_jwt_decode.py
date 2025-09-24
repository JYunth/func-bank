import pytest
import jwt
import time
from func_bank.jwt_decode import decode_jwt


def test_decode_jwt_success():
    """Test successful decoding of a valid JWT token."""
    payload = {"user": "test", "role": "admin"}
    secret = "secret"
    token = jwt.encode(payload, secret, algorithm="HS256")
    result = decode_jwt(token, secret)
    assert result == payload


def test_decode_jwt_expired_token():
    """Test decoding of an expired JWT token returns None."""
    payload = {"user": "test", "exp": int(time.time()) - 3600}  # Expired 1 hour ago
    secret = "secret"
    token = jwt.encode(payload, secret, algorithm="HS256")
    result = decode_jwt(token, secret)
    assert result is None


def test_decode_jwt_malformed_token():
    """Test decoding of a malformed token raises an error."""
    secret = "secret"
    malformed_token = "invalid.jwt.token"
    with pytest.raises(Exception):
        decode_jwt(malformed_token, secret)