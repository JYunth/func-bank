# Function Contract: generate_embedding

## Signature
```python
def generate_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    """
    Generate vector embedding for input text using specified Ollama model.
    
    Args:
        text (str): Input text to embed
        model (str): Ollama model name for embedding. Defaults to nomic-embed-text.
    
    Returns:
        list[float]: Vector representation of the input text
    
    Raises:
        ValueError: If text is empty or model is invalid
        ConnectionError: If Ollama service is unavailable
    """
```

## Input Validation
- text: non-empty string, unlimited length
- model: valid Ollama model name supporting embeddings

## Output Validation
- Returns list of floats
- Length depends on model (typically 768-4096 dimensions)

## Error Cases
- Empty text: ValueError
- Invalid model: ValueError
- Ollama unavailable: ConnectionError