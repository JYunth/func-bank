import pytest
from func_bank.ollama_integration import simple_chat


def test_simple_chat_response_scenario():
    """Integration test for simple chat response acceptance scenario."""
    # Given a prompt
    prompt = "What is the capital of France?"

    # When I call the simple chat function
    response = simple_chat(prompt)

    # Then I receive an AI-generated response
    assert isinstance(response, str)
    assert len(response) > 0
    assert "paris" in response.lower()  # basic validation