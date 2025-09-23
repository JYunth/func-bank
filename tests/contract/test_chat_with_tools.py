import pytest
from src.ollama_integration import chat_with_tools


def test_chat_with_tools_signature():
    """Test chat_with_tools function signature and basic behavior."""
    prompt = "What's the weather?"
    tools = [{"name": "get_weather", "description": "Get weather", "parameters": {}}]
    result = chat_with_tools(prompt, tools)
    assert isinstance(result, dict)
    assert "content" in result


def test_chat_with_tools_empty_prompt():
    """Test chat_with_tools with empty prompt raises ValueError."""
    tools = [{"name": "test", "description": "test", "parameters": {}}]
    with pytest.raises(ValueError):
        chat_with_tools("", tools)


def test_chat_with_tools_invalid_tools():
    """Test chat_with_tools with invalid tools raises ValueError."""
    with pytest.raises(ValueError):
        chat_with_tools("test", [])  # empty tools

    with pytest.raises(ValueError):
        chat_with_tools("test", [{"invalid": "format"}])


def test_chat_with_tools_invalid_model():
    """Test chat_with_tools with invalid model raises ValueError."""
    tools = [{"name": "test", "description": "test", "parameters": {}}]
    with pytest.raises(ValueError):
        chat_with_tools("test", tools, model="invalid_model")