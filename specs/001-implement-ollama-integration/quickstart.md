# Quickstart: Ollama Integration Components

## Prerequisites
- Python 3.11+
- Ollama installed and running locally
- Required models pulled: `ollama pull nomic-embed-text` and `ollama pull llama3.2`

## Installation
```bash
pip install ollama
```

## Basic Usage Examples

### Embedding Generation
```python
from ollama_integration import generate_embedding

text = "Hello, world!"
vector = generate_embedding(text)
print(f"Embedding dimension: {len(vector)}")
```

### Simple Chat
```python
from ollama_integration import simple_chat

response = simple_chat("What is the capital of France?")
print(response)  # Expected: "The capital of France is Paris."
```

### Chat with History
```python
from ollama_integration import chat_with_history

history = [
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "Hello Alice! How can I help you today?"}
]
response = chat_with_history(history, "What's my name?")
print(response)  # Should remember "Alice"
```

### Chat with Tools
```python
from ollama_integration import chat_with_tools

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

## Validation Test
Run this to verify everything works:
```python
# Test all functions with basic inputs
try:
    emb = generate_embedding("test")
    chat = simple_chat("hello")
    hist = chat_with_history([{"role": "user", "content": "hi"}])
    tools = chat_with_tools("time?", [])
    print("All functions working!")
except Exception as e:
    print(f"Error: {e}")
```