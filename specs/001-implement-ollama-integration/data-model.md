# Data Model: Ollama Integration Components

## Entities

### Conversation History
- **Purpose**: Stores conversation context for chat with history functionality
- **Structure**:
  ```python
  [
    {
      "role": "user" | "assistant",
      "content": str,
      "timestamp": datetime (optional),
      "model": str (optional)
    }
  ]
  ```
- **Validation Rules**:
  - role: Must be "user" or "assistant"
  - content: Non-empty string
  - timestamp: ISO format datetime if present
  - model: Valid Ollama model name if present
- **Relationships**: Used as input to chat_with_history function
- **State Transitions**: N/A (static data structure)

### Embedding Vector
- **Purpose**: Numerical representation of text for similarity operations
- **Structure**: `list[float]` (variable length based on model)
- **Validation Rules**: Non-empty list of floats
- **Relationships**: Output of generate_embedding function

### Tool Definition
- **Purpose**: Defines available tools for chat with tools functionality
- **Structure**:
  ```python
  {
    "name": str,
    "description": str,
    "parameters": dict  # JSON schema
  }
  ```
- **Validation Rules**: name and description required, parameters as valid JSON schema
- **Relationships**: Input to chat_with_tools function

### Chat Response
- **Purpose**: AI-generated response from chat functions
- **Structure**: `str` for simple responses, `dict` for tool-enabled responses
- **Validation Rules**: Non-empty string or dict with expected keys
- **Relationships**: Output of chat functions