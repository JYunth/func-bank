import pytest
import pytest
from func_bank.ollama_integration import chat_with_tools
from func_bank.exceptions import ValidationError


def test_chat_with_tools_signature():
    """Test chat_with_tools function signature and basic behavior."""
    prompt = "What's the weather?"
    tools = [{"name": "get_weather", "description": "Get weather", "parameters": {}}]
    result = chat_with_tools(prompt, tools)
    assert isinstance(result, dict)
    assert "content" in result


def test_chat_with_tools_empty_prompt():
    """Test chat_with_tools with empty prompt raises ValidationError."""
    tools = [{"name": "test", "description": "test", "parameters": {}}]
    with pytest.raises(ValidationError):
        chat_with_tools("", tools)


def test_chat_with_tools_invalid_tools():
    """Test chat_with_tools with invalid tools raises ValidationError."""
    with pytest.raises(ValidationError):
        chat_with_tools("test", [])  # empty tools

    with pytest.raises(ValidationError):
        chat_with_tools("test", [{"invalid": "format"}])


def test_chat_with_tools_invalid_model():
    """Test chat_with_tools with invalid model raises ValidationError."""
    tools = [{"name": "test", "description": "test", "parameters": {}}]
    with pytest.raises(ValidationError):
        chat_with_tools("test", tools, model="invalid_model")