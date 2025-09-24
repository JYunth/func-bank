import pytest
from func_bank.ollama_integration import simple_chat
from func_bank.exceptions import ValidationError


def test_simple_chat_signature():
    """Test simple_chat function signature and basic behavior."""
    prompt = "What is 2+2?"
    result = simple_chat(prompt)
    assert isinstance(result, str)
    assert len(result) > 0


def test_simple_chat_empty_prompt():
    """Test simple_chat with empty prompt raises ValidationError."""
    with pytest.raises(ValidationError):
        simple_chat("")


def test_simple_chat_invalid_model():
    """Test simple_chat with invalid model raises ValidationError."""
    with pytest.raises(ValidationError):
        simple_chat("test", model="invalid_model")