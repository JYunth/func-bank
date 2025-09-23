#!/usr/bin/env python3
"""
Interactive Agentic Chat with JSONPlaceholder Tools

This script provides an interactive chat interface where you can converse with an AI
that has access to JSONPlaceholder API tools. The AI can:

- Get specific posts by ID
- Create new posts
- List posts (optionally filtered by user)

Type your messages and the AI will respond, using tools when appropriate.
Type 'quit', 'exit', or 'bye' to end the conversation.
"""

import logging
from typing import List, Dict, Any, Optional
import ollama
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Copy-pasted functions from src/ollama_integration.py
def chat_with_history(history: List[Dict[str, Any]], model: str = "llama3.2") -> str:
    """Generate AI response considering conversation history."""
    if not history or not isinstance(history, list):
        raise ValueError("History must be a non-empty list")

    # Validate history format
    for msg in history:
        if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
            raise ValueError("Each history message must have 'role' and 'content' keys")
        if msg["role"] not in ["user", "assistant", "tool"]:
            raise ValueError("Message role must be 'user', 'assistant', or 'tool'")
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


def execute_tool_call(tool_call) -> Any:
    """Execute a tool call from chat_with_tools response"""
    print(f"  🔍 Raw tool_call object: {tool_call} (type: {type(tool_call)})")

    # Handle different possible formats from Ollama
    function_name = ""
    arguments = {}

    # Check if tool_call is a tuple/list and extract the dict
    if isinstance(tool_call, (tuple, list)) and len(tool_call) > 0:
        tool_call = tool_call[0]
        print(f"  🔍 Extracted from tuple: {tool_call}")

    # Try different possible formats
    if isinstance(tool_call, dict):
        if "function" in tool_call:
            function_name = tool_call["function"].get("name", "")
            arguments = tool_call["function"].get("arguments", {})
        elif "name" in tool_call:
            function_name = tool_call.get("name", "")
            arguments = tool_call.get("arguments", {})
        else:
            # Direct arguments dict
            arguments = tool_call
    else:
        return {"error": f"Unexpected tool_call format: {tool_call}"}

    print(f"  🔍 Parsed - name: '{function_name}', args: {arguments}")

    # Primary: Use exact tool names and parameters as defined
    if function_name == "get_post":
        post_id = arguments.get("post_id")
        if isinstance(post_id, int):
            return get_jsonplaceholder_post(post_id)
        else:
            return {"error": f"get_post requires integer post_id, got: {post_id}"}
    elif function_name == "create_post":
        title = arguments.get("title")
        body = arguments.get("body")
        user_id = arguments.get("user_id", 1)
        if isinstance(title, str) and isinstance(body, str) and isinstance(user_id, int):
            return create_jsonplaceholder_post(title, body, user_id)
        else:
            return {"error": f"create_post requires title (str) and body (str), got: title={title}, body={body}"}
    elif function_name == "list_posts":
        user_id = arguments.get("user_id")
        limit = arguments.get("limit", 5)
        if user_id is not None and not isinstance(user_id, int):
            user_id = None
        if not isinstance(limit, int):
            limit = 5
        return list_jsonplaceholder_posts(user_id, limit)

    # Fallback: Try to infer from arguments (for when AI doesn't follow instructions)
    if not function_name:
        if "post_id" in arguments and isinstance(arguments["post_id"], int):
            return get_jsonplaceholder_post(arguments["post_id"])
        elif "id" in arguments and isinstance(arguments["id"], str):
            try:
                post_id = int(arguments["id"])
                return get_jsonplaceholder_post(post_id)
            except ValueError:
                pass
        elif "title" in arguments and "body" in arguments:
            title = arguments["title"]
            body = arguments["body"]
            user_id = arguments.get("user_id", 1)
            if isinstance(title, str) and isinstance(body, str):
                return create_jsonplaceholder_post(title, body, user_id)

    return {"error": f"Unknown or invalid tool call: {function_name} with args {arguments}"}


class AgenticChatManager:
    """Agentic chat manager that properly handles tool calls and continues conversation"""

    def __init__(self, tools: List[Dict[str, Any]], model: str = "llama3.2"):
        self.tools = tools
        self.model = model
        self.history: List[Dict[str, Any]] = []
        self.max_iterations = 5  # Prevent infinite loops

        # Check if model supports tools
        self._check_model_supports_tools()

        # Strong system prompt to enforce correct tool usage
        self.system_prompt = self._create_system_prompt()

    def _check_model_supports_tools(self):
        """Check if the model supports tool calling"""
        try:
            # Try to get model info
            info = ollama.show(self.model)
            print(f"🤖 Using model: {self.model}")
            if "template" in info and "# Tools:" in info.get("template", ""):
                print("✅ Model supports tool calling")
            else:
                print("⚠️ Model may not fully support tool calling - results may vary")
        except Exception as e:
            print(f"⚠️ Could not verify model tool support: {e}")

    def _create_system_prompt(self) -> str:
        """Create a strong system prompt that enforces correct tool usage"""
        tool_descriptions = []
        for tool in self.tools:
            name = tool["name"]
            desc = tool["description"]
            params = tool.get("parameters", {}).get("properties", {})
            required = tool.get("parameters", {}).get("required", [])

            # Format parameters
            param_list = []
            for param_name, param_info in params.items():
                param_type = param_info.get("type", "string")
                param_desc = param_info.get("description", "")
                required_mark = "*" if param_name in required else ""
                param_list.append(f"  - {param_name}{required_mark}: {param_type} - {param_desc}")

            tool_descriptions.append(f"""• {name}: {desc}
{chr(10).join(param_list)}""")

        return f"""You are a helpful AI assistant with access to JSONPlaceholder API tools.

You can use these tools to interact with the JSONPlaceholder API for blog posts:

AVAILABLE TOOLS:
{chr(10).join(tool_descriptions)}

TOOL USAGE:
- Use get_post when the user wants to see a specific post by ID
- Use list_posts when the user wants to see multiple posts or filter by user
- Use create_post when the user wants to add a new post

Always use the exact tool names and parameter names as specified above.
If you need to use a tool, call it with the proper format."""

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
                print(f"💬 AI: {ai_content}")
                return ai_content

            # Execute tool calls (let the LLM decide what's appropriate)
            print(f"🔧 Executing {len(tool_calls)} tool call(s)...")
            for i, tool_call in enumerate(tool_calls):
                print(f"  🔧 Tool call #{i+1}: {tool_call}")
                tool_result = execute_tool_call(tool_call)
                print(f"  📄 Tool result: {tool_result}")

                # Add tool result to history
                self.history.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call.get("id", f"call_{i}")
                })

        # If we hit max iterations, return the last response
        print(f"💬 AI: {ai_content}")
        return ai_content if ai_content else "I couldn't complete the task within the allowed iterations."

    def _detect_intent_and_call_tool(self, user_message: str):
        """Fallback intent detection when AI tool calls fail"""
        import re

        message = user_message.lower()

        # Detect "get post X" or "get the Xth post"
        get_post_match = re.search(r'get(?:\s+the)?\s+(\d+)(?:st|nd|rd|th)?\s+post', message)
        if get_post_match:
            post_id = int(get_post_match.group(1))
            print(f"  🎯 Detected intent: get_post(post_id={post_id})")
            return get_jsonplaceholder_post(post_id)

        # Detect "show me post X"
        show_post_match = re.search(r'(?:show|give)\s+me\s+post\s+(\d+)', message)
        if show_post_match:
            post_id = int(show_post_match.group(1))
            print(f"  🎯 Detected intent: get_post(post_id={post_id})")
            return get_jsonplaceholder_post(post_id)

        # Detect "list first X posts" or "show X posts"
        list_posts_match = re.search(r'(?:list|show)(?:\s+the)?\s+(?:first\s+)?(\d+)\s+posts', message)
        if list_posts_match:
            limit = int(list_posts_match.group(1))
            print(f"  🎯 Detected intent: list_posts(limit={limit})")
            return list_jsonplaceholder_posts(limit=limit)

        # Detect "posts by user X"
        user_posts_match = re.search(r'posts\s+by\s+user\s+(\d+)', message)
        if user_posts_match:
            user_id = int(user_posts_match.group(1))
            print(f"  🎯 Detected intent: list_posts(user_id={user_id})")
            return list_jsonplaceholder_posts(user_id=user_id)

        # Detect "create a post about X"
        create_match = re.search(r'create\s+a?\s+post\s+about\s+(.+)', message)
        if create_match:
            topic = create_match.group(1).strip()
            print(f"  🎯 Detected intent: create_post about '{topic}'")
            return create_jsonplaceholder_post(
                title=f"Post about {topic}",
                body=f"This is a post about {topic}."
            )

        return None  # No intent detected



    def _call_ai_with_tools(self) -> Dict[str, Any]:
        """Call AI with current history and tools"""
        try:
            # Always include system prompt as the first message
            messages = [{"role": "system", "content": self.system_prompt}] + self.history
            response = ollama.chat(model=self.model, messages=messages, tools=self.tools)

            result = {"content": response["message"]["content"]}

            # Check for tool calls (format may vary)
            if "tool_calls" in response["message"]:
                tool_calls = response["message"]["tool_calls"]
                print(f"  📋 Raw tool_calls from Ollama: {tool_calls}")
                result["tool_calls"] = tool_calls

            return result
        except Exception as e:
            logger.error(f"AI call failed: {e}")
            return {"content": f"Error: {str(e)}", "tool_calls": []}


def print_welcome():
    """Print welcome message and instructions"""
    print("🤖 Interactive Agentic Chat with JSONPlaceholder Tools")
    print("=" * 60)
    print()
    print("I can help you interact with the JSONPlaceholder API using these tools:")
    print("• Get a specific post by ID")
    print("• Create new posts")
    print("• List posts (optionally filtered by user)")
    print()
    print("Try asking me things like:")
    print("• 'Get the post with ID 5'")
    print("• 'Create a post about Python programming'")
    print("• 'Show me the first 3 posts'")
    print("• 'List posts by user 2'")
    print()
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("-" * 60)


def main():
    """Main interactive chat loop"""
    try:
        # Initialize the agentic chat manager
        agent = AgenticChatManager(JSONPLACEHOLDER_TOOLS)

        print_welcome()

        while True:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n👋 Goodbye! Thanks for chatting.")
                break

            # Skip empty input
            if not user_input:
                continue

            # Process the message
            try:
                agent.chat(user_input)
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please make sure Ollama is running and the required models are available.")

    except KeyboardInterrupt:
        print("\n\n👋 Chat interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Make sure Ollama is running with the required models:")
        print("  ollama serve")
        print("  ollama pull llama3.2")


if __name__ == "__main__":
    main()