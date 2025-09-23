# Function Contract: chat_with_tools

## Signature
```python
def chat_with_tools(prompt: str, tools: list[dict], model: str = "llama3.2") -> dict:
    """
    Generate AI response that may include tool calls.
    
    Args:
        prompt (str): User prompt text
        tools (list[dict]): List of tool definitions
        model (str): Ollama model name for chat. Defaults to llama3.2.
    
    Returns:
        dict: Response containing 'content' and optionally 'tool_calls'
    
    Raises:
        ValueError: If prompt is empty, tools invalid, or model invalid
        ConnectionError: If Ollama service is unavailable
    """
```

## Input Validation
- prompt: non-empty string
- tools: list of dicts with name, description, parameters
- model: valid Ollama chat model name

## Output Validation
- Returns dict with 'content' key, optionally 'tool_calls' list

## Error Cases
- Empty prompt: ValueError
- Invalid tools: ValueError
- Invalid model: ValueError
- Ollama unavailable: ConnectionError