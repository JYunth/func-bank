import pytest
from src.ollama_integration import generate_embedding, simple_chat, chat_with_history, chat_with_tools


def test_generate_embedding_validation():
    """Unit test for generate_embedding input validation."""
    # Valid input should not raise
    try:
        # This will fail due to no Ollama, but validation should pass
        generate_embedding("test")
    except ConnectionError:
        pass  # Expected if Ollama not running
    except ValueError:
        pytest.fail("Valid input should not raise ValueError")

    # Invalid inputs
    with pytest.raises(ValueError, match="Text cannot be empty"):
        generate_embedding("")

    with pytest.raises(ValueError, match="Text cannot be empty"):
        generate_embedding("   ")


def test_simple_chat_validation():
    """Unit test for simple_chat input validation."""
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        simple_chat("")

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        simple_chat("   ")


def test_chat_with_history_validation():
    """Unit test for chat_with_history input validation."""
    with pytest.raises(ValueError, match="History must be a non-empty list"):
        chat_with_history([])

    with pytest.raises(ValueError, match="History must be a non-empty list"):
        chat_with_history(None)

    with pytest.raises(ValueError, match="Each history message must have"):
        chat_with_history([{"invalid": "format"}])

    with pytest.raises(ValueError, match="Message role must be"):
        chat_with_history([{"role": "invalid", "content": "test"}])

    with pytest.raises(ValueError, match="Message content must be"):
        chat_with_history([{"role": "user", "content": ""}])


def test_chat_with_tools_validation():
    """Unit test for chat_with_tools input validation."""
    tools = [{"name": "test", "description": "test", "parameters": {}}]

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        chat_with_tools("", tools)

    with pytest.raises(ValueError, match="Tools must be a non-empty list"):
        chat_with_tools("test", [])

    with pytest.raises(ValueError, match="Each tool must have"):
        chat_with_tools("test", [{"invalid": "format"}])