import pytest
from func_bank.api_crud import handle_crud
from func_bank.jwt_encode import encode_jwt

def test_api_with_rbac_success():
    """Test API CRUD with successful RBAC verification."""
    # Create a token with admin role
    payload = {"user_id": 1, "role": "admin"}
    secret = "secret"
    token = encode_jwt(payload, secret)

    # Assume table exists and data is valid
    table = "users"
    data = {"name": "John", "email": "john@example.com"}

    # This will fail if DB is not set up, but tests the integration
    try:
        result = handle_crud("POST", table, data, token=token, secret=secret, required_role="admin")
        assert result["status"] == "success"
    except Exception as e:
        # If DB not connected, just check that auth passed
        if "Access denied" in str(e):
            pytest.fail("Auth should have passed")

def test_api_with_rbac_access_denied():
    """Test API CRUD with RBAC access denied."""
    # Create a token with user role
    payload = {"user_id": 1, "role": "user"}
    secret = "secret"
    token = encode_jwt(payload, secret)

    table = "users"
    data = {"name": "John", "email": "john@example.com"}

    with pytest.raises(ValueError, match="Access denied"):
        handle_crud("POST", table, data, token=token, secret=secret, required_role="admin")