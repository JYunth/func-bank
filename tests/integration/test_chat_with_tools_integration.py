import pytest
from src.ollama_integration import chat_with_tools


def test_chat_with_tools_scenario():
    """Integration test for chat with tools acceptance scenario."""
    # Given a prompt and tool definitions
    prompt = "What's the weather in Paris?"
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    ]

    # When I call the chat with tools function
    response = chat_with_tools(prompt, tools)

    # Then I receive a response that may include tool calls
    assert isinstance(response, dict)
    assert "content" in response
    assert isinstance(response["content"], str)

    # May or may not have tool_calls depending on model decision
    if "tool_calls" in response:
        assert isinstance(response["tool_calls"], list)