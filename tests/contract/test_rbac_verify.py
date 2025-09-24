import pytest
from func_bank.rbac_verify import verify_role
from func_bank.jwt_encode import encode_jwt

def test_verify_role_success():
    payload = {"role": "admin"}
    secret = "secret"
    token = encode_jwt(payload, secret)
    required_role = "admin"
    result = verify_role(token, required_role, secret)
    assert result is True

def test_verify_role_invalid_token():
    with pytest.raises(Exception):  # Well-documented error
        verify_role("invalid_token", "admin", "secret")

def test_verify_role_mismatch():
    payload = {"role": "user"}
    secret = "secret"
    token = encode_jwt(payload, secret)
    required_role = "admin"
    result = verify_role(token, required_role, secret)
    assert result is False