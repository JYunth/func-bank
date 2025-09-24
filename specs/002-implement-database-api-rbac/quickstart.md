# Quick Start Guide

## Installation
```bash
uv add sqlalchemy psycopg2 PyJWT
```

## Database Setup
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
```

## Usage Examples

### Database CRUD
```python
from db_create import create_record
from db_read import read_record

id = create_record("users", {"name": "John", "email": "john@example.com"})
user = read_record("users", id)
```

### JWT
```python
from jwt_encode import encode_jwt
from jwt_decode import decode_jwt

token = encode_jwt({"user_id": 1, "role": "admin"}, "secret")
payload = decode_jwt(token, "secret")
```

### RBAC
```python
from rbac_verify import verify_role

if verify_role(token, "admin", "secret"):
    # allow access
```

## Error Handling
All functions throw well-documented errors. Catch and handle in main code.

## Integration
Components work together: API uses DB and RBAC for secure CRUD operations.
