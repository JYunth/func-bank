import pytest
from func_bank.jwt_encode import encode_jwt

def test_encode_jwt_success():
    # This test will fail until implementation
    payload = {"user": "test", "role": "admin"}
    secret = "my_secret_key"
    result = encode_jwt(payload, secret)
    assert isinstance(result, str)
    assert len(result) > 0  # JWT should not be empty

def test_encode_jwt_invalid_payload():
    with pytest.raises(Exception):  # Well-documented error
        encode_jwt("not_a_dict", "secret")

def test_encode_jwt_invalid_secret():
    with pytest.raises(Exception):  # Well-documented error
        encode_jwt({"user": "test"}, 123)