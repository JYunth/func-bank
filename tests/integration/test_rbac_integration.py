import pytest
from func_bank.jwt_encode import encode_jwt
from func_bank.rbac_verify import verify_role

def test_rbac_integration_success():
    """Test successful RBAC verification when role matches."""
    payload = {"user_id": 1, "role": "admin"}
    secret = "secret"
    token = encode_jwt(payload, secret)
    result = verify_role(token, "admin", secret)
    assert result is True

def test_rbac_integration_access_denied():
    """Test access denied when role does not match required role."""
    payload = {"user_id": 1, "role": "user"}
    secret = "secret"
    token = encode_jwt(payload, secret)
    result = verify_role(token, "admin", secret)
    assert result is False