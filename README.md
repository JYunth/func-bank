# Func Bank

A collection of copy-pastable functions for common development tasks.

## ✅ Completed Features

### Ollama Integration Components
Self-contained Python functions for integrating Ollama AI models into your applications.
- **Status**: ✅ Fully implemented and tested
- **Functions**: generate_embedding, simple_chat, chat_with_history, chat_with_tools
- **Tests**: 21 passing tests with full coverage
- **GPU Support**: Automatic NVIDIA GPU acceleration

### Installation

```bash
pip install ollama
# Ensure Ollama is running locally
ollama serve
# Pull required models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Usage

#### Embedding Generation

```python
from src.ollama_integration import generate_embedding

text = "Hello, world!"
vector = generate_embedding(text)
print(f"Embedding dimension: {len(vector)}")
```

#### Simple Chat

```python
from src.ollama_integration import simple_chat

response = simple_chat("What is the capital of France?")
print(response)
```

#### Chat with History

```python
from src.ollama_integration import chat_with_history

history = [
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "Hello Alice!"}
]
response = chat_with_history(history, "What's my name?")
print(response)
```

#### Chat with Tools

```python
from src.ollama_integration import chat_with_tools

tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}
    }
]

response = chat_with_tools("What's the weather in Paris?", tools)
print(response)
```

### Error Handling

All functions raise `ValueError` for invalid inputs and `ConnectionError` for Ollama service issues.

### Testing

```bash
pip install pytest
pytest tests/
```

### Features

- ✅ Copy-pastable functions
- ✅ Agnostic design (model-agnostic)
- ✅ Self-contained implementations
- ✅ Comprehensive error handling
- ✅ Type hints and documentation
- ✅ Full test coverage
- ✅ GPU acceleration support
- ✅ Production-ready implementation

### Status

- **Implementation**: ✅ Complete
- **Testing**: ✅ All tests passing (21/21)
- **Validation**: ✅ Functional verification complete
- **Documentation**: ✅ Updated and current