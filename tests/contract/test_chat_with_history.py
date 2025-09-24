import pytest
from func_bank.ollama_integration import chat_with_history
from func_bank.exceptions import ValidationError


def test_chat_with_history_signature():
    """Test chat_with_history function signature and basic behavior."""
    history = [{"role": "user", "content": "Hello"}]
    result = chat_with_history(history)
    assert isinstance(result, str)
    assert len(result) > 0


def test_chat_with_history_invalid_history():
    """Test chat_with_history with invalid history raises ValidationError."""
    with pytest.raises(ValidationError):
        chat_with_history([])  # empty history

    with pytest.raises(ValidationError):
        chat_with_history([{"invalid": "format"}])


def test_chat_with_history_invalid_model():
    """Test chat_with_history with invalid model raises ValidationError."""
    history = [{"role": "user", "content": "test"}]
    with pytest.raises(ValidationError):
        chat_with_history(history, model="invalid_model")