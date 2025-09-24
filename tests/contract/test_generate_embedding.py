import pytest
from func_bank.ollama_integration import generate_embedding
from func_bank.exceptions import ValidationError


def test_generate_embedding_signature():
    """Test generate_embedding function signature and basic behavior."""
    # This test will fail until the function is implemented
    text = "Hello, world!"
    result = generate_embedding(text)
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(x, float) for x in result)


def test_generate_embedding_empty_text():
    """Test generate_embedding with empty text raises ValidationError."""
    with pytest.raises(ValidationError):
        generate_embedding("")


def test_generate_embedding_invalid_model():
    """Test generate_embedding with invalid model raises ValidationError."""
    with pytest.raises(ValidationError):
        generate_embedding("test", model="invalid_model")