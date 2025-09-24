import pytest
from func_bank.ollama_integration import chat_with_history


def test_chat_with_history_scenario():
    """Integration test for chat with history acceptance scenario."""
    # Given a conversation history including the current prompt
    history = [
        {"role": "user", "content": "My name is Alice"},
        {"role": "assistant", "content": "Hello Alice! How can I help you today?"},
        {"role": "user", "content": "What's my name?"}
    ]

    # When I call the chat with history function
    response = chat_with_history(history)

    # Then I receive a context-aware response
    assert isinstance(response, str)
    assert len(response) > 0
    assert "alice" in response.lower()  # should remember the name