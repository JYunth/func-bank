"""
Combined example demonstrating all Ollama integration functions
- generate_embedding: Text to vector conversion
- simple_chat: Basic AI responses
- chat_with_history: Conversational AI with memory
- chat_with_tools: AI with function calling capabilities

This example uses runtime dict storage for conversation history
and includes a JSONPlaceholder API tool for demonstration.
"""

import logging
from typing import List, Dict, Any, Optional
import ollama
import requests  # For JSONPlaceholder API calls

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Copy-pasted functions from src/ollama_integration.py
def generate_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    """Generate vector embedding for input text using specified Ollama model."""
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValueError(f"Invalid model '{model}'")

    try:
        response = ollama.embeddings(model=model, prompt=text)
        return response["embedding"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ConnectionError("Ollama service is unavailable")


def simple_chat(prompt: str, model: str = "llama3.2") -> str:
    """Generate AI response to a single prompt using specified Ollama model."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValueError(f"Invalid model '{model}'")

    try:
        response = ollama.chat(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ConnectionError("Ollama service is unavailable")


def chat_with_history(history: List[Dict[str, Any]], model: str = "llama3.2") -> str:
    """Generate AI response considering conversation history."""
    if not history or not isinstance(history, list):
        raise ValueError("History must be a non-empty list")

    # Validate history format
    for msg in history:
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            raise ValueError("Each history message must have 'role' and 'content' keys")
        if msg["role"] not in ["user", "assistant"]:
            raise ValueError("Message role must be 'user' or 'assistant'")
        if not msg["content"] or not isinstance(msg["content"], str):
            raise ValueError("Message content must be a non-empty string")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValueError(f"Invalid model '{model}'")

    try:
        response = ollama.chat(model=model, messages=history)
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ConnectionError("Ollama service is unavailable")


def chat_with_tools(
    prompt: str, tools: List[Dict[str, Any]], model: str = "llama3.2"
) -> Dict[str, Any]:
    """Generate AI response that may include tool calls."""
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    if not tools or not isinstance(tools, list):
        raise ValueError("Tools must be a non-empty list")

    # Validate tools format
    for tool in tools:
        if (
            not isinstance(tool, dict)
            or "name" not in tool
            or "description" not in tool
        ):
            raise ValueError("Each tool must have 'name' and 'description' keys")

    try:
        ollama.show(model)
    except Exception as e:
        logger.error(f"Invalid model '{model}': {e}")
        raise ValueError(f"Invalid model '{model}'")

    try:
        messages = [{"role": "user", "content": prompt}]
        response = ollama.chat(model=model, messages=messages, tools=tools)

        result = {"content": response["message"]["content"]}

        # Check for tool calls (format may vary)
        if "tool_calls" in response["message"]:
            result["tool_calls"] = response["message"]["tool_calls"]

        return result
    except Exception as e:
        logger.error(f"Ollama service error: {e}")
        raise ConnectionError("Ollama service is unavailable")


# Runtime conversation history storage (in-memory dict)
class ConversationManager:
    """Simple in-memory conversation history storage"""

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append({"role": role, "content": content})

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversations.get(conversation_id, [])

    def chat(self, conversation_id: str, message: str, model: str = "llama3.2") -> str:
        """Chat with history persistence"""
        self.add_message(conversation_id, "user", message)
        history = self.get_history(conversation_id)
        response = chat_with_history(history, model)
        self.add_message(conversation_id, "assistant", response)
        return response


class AgenticChatManager:
    """Agentic chat manager that properly handles tool calls and continues conversation"""

    def __init__(self, tools: List[Dict[str, Any]], model: str = "llama3.2"):
        self.tools = tools
        self.model = model
        self.history: List[Dict[str, Any]] = []
        self.max_iterations = 5  # Prevent infinite loops

    def chat(self, user_message: str) -> str:
        """Have a conversation with tool calling capabilities"""
        # Add user message to history
        self.history.append({"role": "user", "content": user_message})

        ai_content = ""  # Initialize to avoid unbound variable

        for iteration in range(self.max_iterations):
            print(f"🤖 AI thinking (iteration {iteration + 1})...")

            # Get AI response (may include tool calls)
            response = self._call_ai_with_tools()

            ai_content = response.get("content", "")
            tool_calls = response.get("tool_calls", [])

            # Add AI response to history
            self.history.append({"role": "assistant", "content": ai_content})

            # If no tool calls, we're done
            if not tool_calls:
                print(f"💬 AI final response: {ai_content}")
                return ai_content

            # Execute tool calls and add results to history
            print(f"🔧 Executing {len(tool_calls)} tool call(s)...")
            for tool_call in tool_calls:
                tool_result = execute_tool_call(tool_call)
                print(f"  📄 Tool result: {tool_result}")

                # Add tool result to history
                self.history.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call.get("id", "")
                })

        # If we hit max iterations, return the last response
        return ai_content if ai_content else "I couldn't complete the task within the allowed iterations."

    def _call_ai_with_tools(self) -> Dict[str, Any]:
        """Call AI with current history and tools"""
        try:
            messages = self.history
            response = ollama.chat(model=self.model, messages=messages, tools=self.tools)

            result = {"content": response["message"]["content"]}

            # Check for tool calls (format may vary)
            if "tool_calls" in response["message"]:
                result["tool_calls"] = response["message"]["tool_calls"]

            return result
        except Exception as e:
            logger.error(f"AI call failed: {e}")
            return {"content": f"Error: {str(e)}", "tool_calls": []}


# JSONPlaceholder API tool functions
def get_jsonplaceholder_post(post_id: int) -> Dict[str, Any]:
    """Get a specific post from JSONPlaceholder"""
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to get post {post_id}: {str(e)}"}


def create_jsonplaceholder_post(title: str, body: str, user_id: int = 1) -> Dict[str, Any]:
    """Create a new post on JSONPlaceholder"""
    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json={"title": title, "body": body, "userId": user_id},
            headers={"Content-type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to create post: {str(e)}"}


def list_jsonplaceholder_posts(user_id: Optional[int] = None, limit: int = 5) -> List[Dict[str, Any]]:
    """List posts from JSONPlaceholder, optionally filtered by user"""
    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        params = {}
        if user_id:
            params["userId"] = user_id

        response = requests.get(url, params=params)
        response.raise_for_status()
        posts = response.json()
        return posts[:limit]  # Limit results
    except Exception as e:
        return [{"error": f"Failed to list posts: {str(e)}"}]


# Tool definitions for chat_with_tools
JSONPLACEHOLDER_TOOLS = [
    {
        "name": "get_post",
        "description": "Get a specific post by ID from JSONPlaceholder",
        "parameters": {
            "type": "object",
            "properties": {
                "post_id": {"type": "integer", "description": "The post ID to retrieve"}
            },
            "required": ["post_id"]
        }
    },
    {
        "name": "create_post",
        "description": "Create a new post on JSONPlaceholder",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Post title"},
                "body": {"type": "string", "description": "Post content"},
                "user_id": {"type": "integer", "description": "User ID (defaults to 1)"}
            },
            "required": ["title", "body"]
        }
    },
    {
        "name": "list_posts",
        "description": "List posts from JSONPlaceholder, optionally filtered by user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "Filter by user ID"},
                "limit": {"type": "integer", "description": "Maximum number of posts to return"}
            }
        }
    }
]


def execute_tool_call(tool_call: Dict[str, Any]) -> Any:
    """Execute a tool call from chat_with_tools response"""
    # Handle different possible formats from Ollama
    function_name = ""
    arguments = {}

    # Try different possible formats
    if "function" in tool_call:
        function_name = tool_call["function"].get("name", "")
        arguments = tool_call["function"].get("arguments", {})
    elif "name" in tool_call:
        function_name = tool_call.get("name", "")
        arguments = tool_call.get("arguments", {})

    # If function name is empty, try to infer from arguments
    if not function_name:
        if "url" in arguments and isinstance(arguments["url"], str) and "posts" in arguments["url"]:
            if "/posts/" in arguments["url"]:
                # Looks like a get_post call
                try:
                    post_id_str = arguments["url"].split("/posts/")[-1]
                    post_id = int(post_id_str)
                    return get_jsonplaceholder_post(post_id)
                except (ValueError, IndexError):
                    return {"error": f"Could not parse post ID from URL: {arguments['url']}"}
            else:
                # Looks like a list_posts call
                return list_jsonplaceholder_posts()
        elif "title" in arguments and "body" in arguments:
            # Looks like a create_post call
            title = arguments["title"]
            body = arguments["body"]
            user_id = arguments.get("user_id", 1)
            if isinstance(title, str) and isinstance(body, str) and isinstance(user_id, int):
                return create_jsonplaceholder_post(title, body, user_id)
            else:
                return {"error": f"Invalid arguments for create_post: {arguments}"}

    # Standard format handling
    if function_name == "get_post":
        post_id = arguments.get("post_id")
        if isinstance(post_id, int):
            return get_jsonplaceholder_post(post_id)
        else:
            return {"error": f"Invalid post_id: {post_id}"}
    elif function_name == "create_post":
        title = arguments.get("title")
        body = arguments.get("body")
        user_id = arguments.get("user_id", 1)
        if isinstance(title, str) and isinstance(body, str):
            return create_jsonplaceholder_post(title, body, user_id)
        else:
            return {"error": f"Invalid title or body: title={title}, body={body}"}
    elif function_name == "list_posts":
        user_id = arguments.get("user_id")
        limit = arguments.get("limit", 5)
        if user_id is not None and not isinstance(user_id, int):
            user_id = None
        if not isinstance(limit, int):
            limit = 5
        return list_jsonplaceholder_posts(user_id, limit)
    else:
        return {"error": f"Unknown tool: {function_name}, arguments: {arguments}"}


def main():
    """Demonstrate all Ollama integration functions"""

    print("🚀 Combined Ollama Integration Example")
    print("=" * 50)

    # 1. Generate Embedding
    print("\n1. 📊 Text Embedding Generation")
    try:
        text = "Hello, this is a test for embedding generation!"
        embedding = generate_embedding(text)
        print(f"Text: {text}")
        print(f"Embedding dimensions: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"Embedding failed: {e}")

    # 2. Simple Chat
    print("\n2. 💬 Simple Chat")
    try:
        question = "What is the capital of France?"
        answer = simple_chat(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
    except Exception as e:
        print(f"Simple chat failed: {e}")

    # 3. Chat with History (using runtime storage)
    print("\n3. 🗣️ Conversational Chat with History")
    try:
        conv_manager = ConversationManager()

        # First message
        response1 = conv_manager.chat("demo_conv", "My name is Alice")
        print("User: My name is Alice")
        print(f"AI: {response1}")

        # Follow-up (AI should remember name)
        response2 = conv_manager.chat("demo_conv", "What's my name?")
        print("User: What's my name?")
        print(f"AI: {response2}")

        # Show conversation history
        history = conv_manager.get_history("demo_conv")
        print(f"Conversation length: {len(history)} messages")

    except Exception as e:
        print(f"Chat with history failed: {e}")

    # 4. Chat with Tools (JSONPlaceholder API) - Agentic Implementation
    print("\n4. 🛠️ Agentic Chat with Tools (JSONPlaceholder API)")
    try:
        # Create an agentic chat manager that handles tool calls properly
        agent = AgenticChatManager(JSONPLACEHOLDER_TOOLS)

        # Example 1: Get a post
        print("Example 1: Getting a post")
        final_response1 = agent.chat("Get the post with ID 1 from JSONPlaceholder")
        print(f"Final AI Response: {final_response1}")

        # Example 2: Create a post
        print("\nExample 2: Creating a post")
        final_response2 = agent.chat("Create a new post titled 'My Test Post' with body 'This is a test'")
        print(f"Final AI Response: {final_response2}")

        # Example 3: Multi-step conversation
        print("\nExample 3: Multi-step conversation")
        agent.chat("List the first 3 posts")
        final_response3 = agent.chat("Now get the details of the second post from that list")
        print(f"Final AI Response: {final_response3}")

    except Exception as e:
        print(f"Agentic chat with tools failed: {e}")

    print("\n" + "=" * 50)
    print("✅ All Ollama integration functions demonstrated!")


if __name__ == "__main__":
    main()