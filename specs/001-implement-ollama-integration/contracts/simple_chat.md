# Function Contract: simple_chat

## Signature
```python
def simple_chat(prompt: str, model: str = "llama3.2") -> str:
    """
    Generate AI response to a single prompt using specified Ollama model.
    
    Args:
        prompt (str): User prompt text
        model (str): Ollama model name for chat. Defaults to llama3.2.
    
    Returns:
        str: AI-generated response text
    
    Raises:
        ValueError: If prompt is empty or model is invalid
        ConnectionError: If Ollama service is unavailable
    """
```

## Input Validation
- prompt: non-empty string
- model: valid Ollama chat model name

## Output Validation
- Returns non-empty string response

## Error Cases
- Empty prompt: ValueError
- Invalid model: ValueError
- Ollama unavailable: ConnectionError