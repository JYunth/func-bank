# Func Bank

A collection of copy-pastable functions for common development tasks, including AI integration, database operations, API handling, and role-based access control.

## ✅ Completed Features

### Ollama Integration Components
Self-contained Python functions for integrating Ollama AI models into your applications.
- **Status**: ✅ Fully implemented and tested
- **Functions**: generate_embedding, simple_chat, chat_with_history, chat_with_tools
- **Tests**: 21 passing tests with full coverage
- **GPU Support**: Automatic NVIDIA GPU acceleration

### Database, API, and RBAC Components
Reusable components for database operations, API handling, and role-based access control.
- **Status**: ✅ Fully implemented and tested
- **Database Functions**: create_record, read_record, update_record, delete_record, query_records, vector_search, store_file, retrieve_file
- **API Functions**: handle_crud, handle_multipart
- **JWT Functions**: encode_jwt, decode_jwt
- **RBAC Functions**: verify_role, verify_role_level
- **Tests**: Comprehensive test coverage

## Installation

### Ollama Components
```bash
pip install ollama
# Ensure Ollama is running locally
ollama serve
# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Database/API/RBAC Components
```bash
pip install sqlalchemy psycopg2 PyJWT
# Or using uv
uv add sqlalchemy psycopg2 PyJWT
```

## Setup

### Database Connection
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:pass@localhost/db")
```

## Usage Examples

### Ollama Integration

#### Embedding Generation
```python
from func_bank.ollama_integration import generate_embedding

text = "Hello, world!"
vector = generate_embedding(text)
print(f"Embedding dimension: {len(vector)}")
```

#### Simple Chat
```python
from func_bank.ollama_integration import simple_chat

response = simple_chat("What is the capital of France?")
print(response)  # Expected: "The capital of France is Paris."
```

#### Chat with History
```python
from func_bank.ollama_integration import chat_with_history

history = [
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "Hello Alice! How can I help you today?"}
]
response = chat_with_history(history, "What's my name?")
print(response)  # Should remember "Alice"
```

#### Chat with Tools
```python
from func_bank.ollama_integration import chat_with_tools

tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}}
        }
    }
]

response = chat_with_tools("What's the weather in Paris?", tools)
if "tool_calls" in response:
    print("Tool call requested:", response["tool_calls"])
else:
    print("Response:", response["content"])
```

### Database Operations

#### Create Record
```python
from func_bank.db_create import create_record

record_id = create_record("users", {"name": "John", "email": "john@example.com"})
print(f"Created record with ID: {record_id}")
```

#### Read Record
```python
from func_bank.db_read import read_record

user = read_record("users", 1)
if user:
    print(f"User: {user}")
else:
    print("User not found")
```

#### Update Record
```python
from func_bank.db_update import update_record

success = update_record("users", 1, {"name": "John Doe"})
print(f"Update successful: {success}")
```

#### Delete Record
```python
from func_bank.db_delete import delete_record

success = delete_record("users", 1)
print(f"Delete successful: {success}")
```

#### Query Records
```python
from func_bank.db_query import query_records

filters = {"active": True}
users = query_records("users", filters, limit=10)
print(f"Found {len(users)} active users")
```

#### Vector Search
```python
from func_bank.db_vector import vector_search

query_vector = [0.1, 0.2, 0.3]  # Your embedding vector
results = vector_search("documents", query_vector, limit=5)
print(f"Found {len(results)} similar documents")
```

#### File Storage
```python
from func_bank.db_files import store_file, retrieve_file

# Store a file
file_id = store_file("example.txt", b"Hello, World!")
print(f"File stored with ID: {file_id}")

# Retrieve a file
file_data = retrieve_file(file_id)
print(f"Retrieved file: {file_data}")
```

### API Handling

#### CRUD API Handler
```python
from func_bank.api_crud import handle_crud

# Example FastAPI route
@app.post("/api/users")
def create_user(request_data: dict):
    response = handle_crud("POST", "users", request_data)
    return response
```

#### Multipart Upload Handler
```python
from func_bank.api_multipart import handle_multipart

# Example FastAPI route
@app.post("/api/upload")
def upload_file(file: UploadFile):
    result = handle_multipart(file)
    return result
```

### JWT Authentication

#### Encode JWT
```python
from func_bank.jwt_encode import encode_jwt

payload = {"user_id": 1, "role": "admin"}
token = encode_jwt(payload, "your-secret-key", expires_in=3600)
print(f"JWT Token: {token}")
```

#### Decode JWT
```python
from func_bank.jwt_decode import decode_jwt

payload = decode_jwt(token, "your-secret-key")
if payload:
    print(f"Decoded payload: {payload}")
else:
    print("Invalid token")
```

### Role-Based Access Control

#### Verify Role
```python
from func_bank.rbac_verify import verify_role

has_access = verify_role(token, "admin", "your-secret-key")
if has_access:
    print("Access granted")
else:
    print("Access denied")
```

#### Verify Role Level
```python
from func_bank.rbac_level import verify_role_level

# Assuming roles have numeric levels (admin=3, user=1)
has_level = verify_role_level(token, 2, "your-secret-key")  # Requires level 2+
if has_level:
    print("Sufficient role level")
else:
    print("Insufficient role level")
```

## Error Handling

All functions raise well-documented errors for various failure conditions:
- `ValueError` for invalid inputs
- `ConnectionError` for service unavailability
- `PermissionError` for access control violations
- Database-specific errors for connection/query failures

## Testing

```bash
pip install pytest
pytest tests/
```

## Features

- ✅ Copy-pastable functions
- ✅ Agnostic design (model-agnostic, database-agnostic)
- ✅ Self-contained implementations
- ✅ Comprehensive error handling
- ✅ Type hints and documentation
- ✅ Full test coverage
- ✅ GPU acceleration support (Ollama)
- ✅ Production-ready implementation
- ✅ Seamless component integration

## Status

- **Ollama Implementation**: ✅ Complete
- **Database/API/RBAC Implementation**: ✅ Complete
- **Testing**: ✅ All tests passing
- **Validation**: ✅ Functional verification complete
- **Documentation**: ✅ Updated and current