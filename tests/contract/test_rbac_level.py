import pytest
from func_bank.rbac_level import verify_role_level
from func_bank.exceptions import ValidationError, AuthenticationError
from func_bank.jwt_encode import encode_jwt

def test_verify_role_level_success():
    # Create a valid token with level >= min_level
    payload = {"level": 5}  # Higher than min_level
    min_level = 3
    secret = "test_secret"
    token = encode_jwt(payload, secret)
    result = verify_role_level(token, min_level, secret)
    assert result is True

def test_verify_role_level_insufficient():
    # Create a valid token with level < min_level
    payload = {"level": 3}  # Lower than min_level
    min_level = 5
    secret = "test_secret"
    token = encode_jwt(payload, secret)
    result = verify_role_level(token, min_level, secret)
    assert result is False

def test_verify_role_level_invalid_level():
    # Invalid level: min_level not int
    token = "some_token"
    min_level = "not_an_int"
    secret = "test_secret"
    with pytest.raises(ValidationError):
        verify_role_level(token, min_level, secret)

def test_verify_role_invalid_token():
    # Test with an invalid or expired token
    token = "invalid_token"
    min_level = 3
    secret = "test_secret"
    with pytest.raises(AuthenticationError):
        verify_role_level(token, min_level, secret)