# Function Contract: chat_with_history

## Signature
```python
def chat_with_history(history: list[dict], model: str = "llama3.2") -> str:
    """
    Generate AI response considering conversation history.
    
    Args:
        history (list[dict]): List of message objects with role, content, etc.
        model (str): Ollama model name for chat. Defaults to llama3.2.
    
    Returns:
        str: AI-generated response text considering history
    
    Raises:
        ValueError: If history is invalid or model is invalid
        ConnectionError: If Ollama service is unavailable
    """
```

## Input Validation
- history: list of dicts with required 'role' and 'content' keys
- model: valid Ollama chat model name

## Output Validation
- Returns non-empty string response

## Error Cases
- Invalid history format: ValueError
- Invalid model: ValueError
- Ollama unavailable: ConnectionError