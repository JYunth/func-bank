import pytest
import time
from func_bank.jwt_encode import encode_jwt
from func_bank.jwt_decode import decode_jwt


def test_jwt_auth_success():
    """Test successful JWT encode and decode flow."""
    payload = {"user_id": 1, "role": "admin"}
    secret = "my_secret_key"
    token = encode_jwt(payload, secret)
    decoded_payload = decode_jwt(token, secret)
    assert decoded_payload is not None
    # Remove exp field for comparison since it's added automatically
    decoded_payload_no_exp = {k: v for k, v in decoded_payload.items() if k != 'exp'}
    assert decoded_payload_no_exp == payload


def test_jwt_auth_expired_token():
    """Test JWT auth flow with expired token."""
    payload = {"user_id": 1, "role": "admin", "exp": int(time.time()) - 3600}  # Expired 1 hour ago
    secret = "my_secret_key"
    token = encode_jwt(payload, secret)
    decoded_payload = decode_jwt(token, secret)
    assert decoded_payload is None