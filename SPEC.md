# API Reference Specification - Detailed

## System Architecture

**Purpose**: Atomic reference functions for rapid integration without documentation lookup
**Database**: PostgreSQL with SQLAlchemy ORM
**Auth**: JWT with role-based access control
**AI**: Ollama local LLM integration

---

## Ollama Components

### `ollama_embedding.py`
**Function**: `generate_embedding(text: str) -> list[float]`
- **Input**: Raw text string to vectorize
- **Output**: Embedding vector as float array (typically 384 or 768 dimensions)
- **Model**: `nomic-embed-text` (configurable)
- **Use Case**: Converting text to vectors for similarity search
- **Error Handling**: Ollama connection errors, model not found

### `ollama_query.py`  
**Function**: `simple_chat(prompt: str) -> str`
- **Input**: Single user prompt string
- **Output**: AI response as plain text
- **Model**: `llama2` or specified model
- **Message Format**: Single user message, no history
- **Use Case**: One-shot questions, stateless interactions

### `ollama_history.py`
**Function**: `chat_with_history(messages: list[dict]) -> str`
- **Input**: Message array with role/content structure
- **Message Format**: `[{'role': 'user'/'assistant', 'content': str}]`
- **Output**: Latest AI response string
- **Use Case**: Conversational AI with context retention
- **History Management**: Caller manages message persistence

### `ollama_tools.py`
**Function**: `chat_with_tools(prompt: str, tools: list[dict]) -> dict`
- **Input**: User prompt + tool definition array
- **Tool Format**: Function schemas with name/description/parameters
- **Output**: Full response dict including potential tool calls
- **Response Structure**: `{message: {content: str}, tool_calls: [...]}`
- **Use Case**: AI function calling, structured responses

---

## Database Components (PostgreSQL + SQLAlchemy)

### `db_create.py`
**Function**: `create_record(table: str, data: dict) -> int`
- **Input**: Table name, data dictionary (column:value pairs)
- **Output**: Auto-generated primary key ID
- **SQL**: INSERT INTO with RETURNING id
- **Connection**: Uses session context manager
- **Validation**: Column existence, data type matching

### `db_read.py`
**Function**: `read_record(table: str, id: int) -> dict | None`
- **Input**: Table name, primary key ID
- **Output**: Record as dictionary or None if not found
- **SQL**: SELECT * WHERE id = ?
- **Serialization**: SQLAlchemy object to dict conversion
- **Relationships**: Optionally include foreign key data

### `db_update.py`
**Function**: `update_record(table: str, id: int, data: dict) -> bool`
- **Input**: Table name, record ID, update data dictionary
- **Output**: True if updated, False if record not found
- **SQL**: UPDATE SET ... WHERE id = ?
- **Validation**: Only update existing columns
- **Timestamps**: Auto-update modified_at if column exists

### `db_delete.py`
**Function**: `delete_record(table: str, id: int) -> bool`
- **Input**: Table name, primary key ID
- **Output**: True if deleted, False if not found
- **SQL**: DELETE FROM WHERE id = ?
- **Soft Delete**: Check for deleted_at column, set timestamp instead
- **Cascading**: Handle foreign key constraints

### `db_query.py`
**Function**: `query_records(table: str, filters: dict, limit: int = 100) -> list[dict]`
- **Input**: Table name, filter conditions, optional limit
- **Filter Format**: `{'column': value, 'column__op': value}` (op: gt, lt, like, in)
- **Output**: Array of matching records as dictionaries
- **SQL**: SELECT with dynamic WHERE clauses
- **Pagination**: Offset/limit support for large datasets

### `db_vector.py`
**Function**: `vector_search(table: str, embedding: list[float], limit: int = 10) -> list[dict]`
- **Input**: Table name, query embedding vector, result limit
- **Output**: Records sorted by cosine similarity with distance scores
- **Vector Column**: Assumes column named 'embedding' or configurable
- **Distance Metric**: Cosine similarity (pgvector extension)
- **Index**: Requires HNSW or IVFFlat index for performance

### `db_files.py`
**Function**: `store_file(filename: str, data: bytes, metadata: dict = {}) -> str`
- **Input**: Original filename, binary data, optional metadata
- **Output**: Unique file ID/path for retrieval
- **Storage**: BYTEA column in files table
- **Metadata**: JSON column for mime_type, size, upload_time
- **Deduplication**: Optional content hash checking

---

## API Components

### `api_crud.py`
**Function**: `handle_crud(method: str, table: str, data: dict = None, id: int = None) -> dict`
- **Input**: HTTP method, table name, request data, optional ID
- **Methods**: GET, POST, PUT, DELETE mapping to DB operations
- **Output**: Standardized response `{success: bool, data: any, error: str}`
- **Validation**: Request data validation before DB calls
- **Status Codes**: Proper HTTP status mapping

### `api_multipart.py`
**Function**: `handle_multipart(request) -> dict`
- **Input**: HTTP request with multipart/form-data
- **Output**: Parsed files and form data
- **File Handling**: Extract filename, content-type, binary data
- **Size Limits**: Configurable max file size validation
- **Multiple Files**: Support for multiple file uploads

---

## RBAC Components

### `jwt_encode.py`
**Function**: `encode_jwt(payload: dict, secret: str, expires_hours: int = 24) -> str`
- **Input**: User data payload, secret key, expiration time
- **Output**: Signed JWT token string
- **Claims**: Standard iat, exp, plus custom user data
- **Algorithm**: HS256 (configurable to RS256)
- **Payload Structure**: `{user_id: int, role: str, permissions: list}`

### `jwt_decode.py`
**Function**: `decode_jwt(token: str, secret: str) -> dict | None`
- **Input**: JWT token string, secret key for verification
- **Output**: Decoded payload dictionary or None if invalid
- **Validation**: Signature verification, expiration check
- **Error Handling**: Expired, invalid signature, malformed tokens
- **Claims Extraction**: Return user_id, role, permissions

### `rbac_verify.py`
**Function**: `verify_role(token: str, required_role: str, secret: str) -> bool`
- **Input**: JWT token, required role string, secret key
- **Output**: True if user has required role or higher
- **Role Hierarchy**: admin > manager > user > guest
- **Token Validation**: Decode token first, then check role
- **Case Sensitivity**: Normalize role comparison

### `rbac_level.py`
**Function**: `verify_role_level(token: str, min_level: int, secret: str) -> bool`
- **Input**: JWT token, minimum numeric role level, secret key
- **Output**: True if user's role level >= minimum required
- **Level Mapping**: admin=4, manager=3, user=2, guest=1
- **Numeric Comparison**: Allows flexible permission checking
- **Default Levels**: Configurable role-to-number mapping

---

## Implementation Standards

### Error Handling
- All functions return None/False for not-found cases
- Database connection errors propagate up
- JWT validation errors return None/False, not exceptions

### Dependencies
- **Ollama**: `ollama` package for LLM interaction
- **Database**: `sqlalchemy`, `psycopg2` for PostgreSQL
- **JWT**: `PyJWT` for token handling
- **API**: Framework-agnostic (FastAPI/Flask compatible)

### Configuration
- Database connection string externalized
- Model names configurable per function
- JWT secrets from environment variables
- Default limits/timeouts parameterized

### Testing Strategy
- Each file includes basic usage example in docstring
