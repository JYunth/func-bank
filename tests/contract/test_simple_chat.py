import pytest
from src.ollama_integration import simple_chat


def test_simple_chat_signature():
    """Test simple_chat function signature and basic behavior."""
    prompt = "What is 2+2?"
    result = simple_chat(prompt)
    assert isinstance(result, str)
    assert len(result) > 0


def test_simple_chat_empty_prompt():
    """Test simple_chat with empty prompt raises ValueError."""
    with pytest.raises(ValueError):
        simple_chat("")


def test_simple_chat_invalid_model():
    """Test simple_chat with invalid model raises ValueError."""
    with pytest.raises(ValueError):
        simple_chat("test", model="invalid_model")