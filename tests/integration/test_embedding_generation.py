import pytest
from src.ollama_integration import generate_embedding


def test_embedding_generation_scenario():
    """Integration test for embedding generation acceptance scenario."""
    # Given a text input
    text = "This is a test document for embedding."

    # When I call the embedding function
    vector = generate_embedding(text)

    # Then I receive a vector representation of the text
    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(x, float) for x in vector)

    # Additional validation
    assert len(vector) >= 384  # typical embedding dimension