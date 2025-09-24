import time
import pytest
from func_bank.jwt_encode import encode_jwt
from func_bank.jwt_decode import decode_jwt
from func_bank.rbac_verify import verify_role
from func_bank.rbac_level import verify_role_level

def test_jwt_performance():
    """Performance test for JWT operations."""
    payload = {"user_id": 1, "role": "admin", "level": 5}
    secret = "test-secret"

    # Encode performance
    start = time.time()
    for _ in range(100):
        token = encode_jwt(payload, secret)
    encode_time = (time.time() - start) / 100

    # Decode performance
    start = time.time()
    for _ in range(100):
        decode_jwt(token, secret)
    decode_time = (time.time() - start) / 100

    # Should be well under 1ms
    assert encode_time < 0.001
    assert decode_time < 0.001

def test_rbac_performance():
    """Performance test for RBAC operations."""
    payload = {"user_id": 1, "role": "admin", "level": 5}
    secret = "test-secret"
    token = encode_jwt(payload, secret)

    # Verify role performance
    start = time.time()
    for _ in range(100):
        verify_role(token, "admin", secret)
    role_time = (time.time() - start) / 100

    # Verify level performance
    start = time.time()
    for _ in range(100):
        verify_role_level(token, 3, secret)
    level_time = (time.time() - start) / 100

    # Should be well under 1ms
    assert role_time < 0.001
    assert level_time < 0.001

# Note: CRUD performance tests require database connection
# TODO: Add CRUD performance tests when DB is available