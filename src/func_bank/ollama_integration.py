"""
Ollama Integration Components

Copy-pastable functions for AI model integration.
Provides embedding generation, simple chat, chat with history, and chat with tools.
"""

import logging
from typing import List, Dict, Any
import ollama
from func_bank.exceptions import ValidationError, ServiceError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    """
    Generate vector embedding for input text using specified Ollama model.

    Args:
        text (str): Input text to embed
        model (str): Ollama model name for embedding. Defaults to nomic-embed-text.

    Returns:
        List[float]: Vector representation of the input text

    Raises:
        ValidationError: If text is empty or model is invalid
        ServiceError: If Ollama service is unavailable
    """
    if not text or not text.strip():
        raise ValidationError("Text cannot be empty")

    try:
        # Check if model exists (this will raise an error if not)
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValidationError(f"Invalid model '{model}'")

    try:
        response = ollama.embeddings(model=model, prompt=text)
        return response["embedding"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ServiceError("Ollama service is unavailable")


def simple_chat(prompt: str, model: str = "llama3.2") -> str:
    """
    Generate AI response to a single prompt using specified Ollama model.

    Args:
        prompt (str): User prompt text
        model (str): Ollama model name for chat. Defaults to llama3.2.

    Returns:
        str: AI-generated response text

    Raises:
        ValidationError: If prompt is empty or model is invalid
        ServiceError: If Ollama service is unavailable
    """
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt cannot be empty")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValidationError(f"Invalid model '{model}'")

    try:
        response = ollama.chat(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ServiceError("Ollama service is unavailable")


def chat_with_history(history: List[Dict[str, Any]], model: str = "llama3.2") -> str:
    """
    Generate AI response considering conversation history.

    Args:
        history (List[Dict[str, Any]]): List of message objects with role, content, etc.
        model (str): Ollama model name for chat. Defaults to llama3.2.

    Returns:
        str: AI-generated response text considering history

    Raises:
        ValidationError: If history is invalid or model is invalid
        ServiceError: If Ollama service is unavailable
    """
    if not history or not isinstance(history, list):
        raise ValidationError("History must be a non-empty list")

    # Validate history format
    for msg in history:
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            raise ValidationError("Each history message must have 'role' and 'content' keys")
        if msg["role"] not in ["user", "assistant"]:
            raise ValidationError("Message role must be 'user' or 'assistant'")
        if not msg["content"] or not isinstance(msg["content"], str):
            raise ValidationError("Message content must be a non-empty string")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValidationError(f"Invalid model '{model}'")

    try:
        response = ollama.chat(model=model, messages=history)
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ServiceError("Ollama service is unavailable")


def chat_with_tools(
    prompt: str, tools: List[Dict[str, Any]], model: str = "llama3.2"
) -> Dict[str, Any]:
    """
    Generate AI response that may include tool calls.

    Args:
        prompt (str): User prompt text
        tools (List[Dict[str, Any]]): List of tool definitions
        model (str): Ollama model name for chat. Defaults to llama3.2.

    Returns:
        Dict[str, Any]: Response containing 'content' and optionally 'tool_calls'

    Raises:
        ValidationError: If prompt is empty, tools invalid, or model invalid
        ServiceError: If Ollama service is unavailable
    """
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt cannot be empty")

    if not tools or not isinstance(tools, list):
        raise ValidationError("Tools must be a non-empty list")

    # Validate tools format
    for tool in tools:
        if (
            not isinstance(tool, dict)
            or "name" not in tool
            or "description" not in tool
        ):
            raise ValidationError("Each tool must have 'name' and 'description' keys")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValidationError(f"Invalid model '{model}'")

    try:
        # Note: Ollama's tool calling support may vary by model
        # This is a basic implementation - advanced tool calling may need model-specific handling
        messages = [{"role": "user", "content": prompt}]

        # Add tools to the request if supported
        response = ollama.chat(model=model, messages=messages, tools=tools)

        result = {"content": response["message"]["content"]}

        # Check for tool calls (format may vary)
        if "tool_calls" in response["message"]:
            result["tool_calls"] = response["message"]["tool_calls"]

        return result
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ServiceError("Ollama service is unavailable")