"""
Example implementations of chat_with_history using different storage backends
"""

import sqlite3
from typing import List, Dict, Any
from src.ollama_integration import chat_with_history


# 1. Runtime Dict-based History Storage
class RuntimeChatHistory:
    """In-memory conversation history using Python dict"""

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}

    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append({"role": role, "content": content})

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific conversation"""
        return self.conversations.get(conversation_id, [])

    def chat(
        self, conversation_id: str, user_message: str, model: str = "llama3.2"
    ) -> str:
        """Send message and get AI response, updating history"""
        # Add user message to history
        self.add_message(conversation_id, "user", user_message)

        # Get current history
        history = self.get_history(conversation_id)

        # Get AI response
        ai_response = chat_with_history(history, model)

        # Add AI response to history
        self.add_message(conversation_id, "assistant", ai_response)

        return ai_response

    def clear_history(self, conversation_id: str):
        """Clear history for a conversation"""
        self.conversations.pop(conversation_id, None)


# 2. SQLite-based History Storage
class SQLiteChatHistory:
    """Persistent conversation history using SQLite"""

    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conversation_id, role, content),
            )
            conn.commit()

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific conversation"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY timestamp",
                (conversation_id,),
            )
            return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

    def chat(
        self, conversation_id: str, user_message: str, model: str = "llama3.2"
    ) -> str:
        """Send message and get AI response, updating history"""
        # Add user message to history
        self.add_message(conversation_id, "user", user_message)

        # Get current history
        history = self.get_history(conversation_id)

        # Get AI response
        ai_response = chat_with_history(history, model)

        # Add AI response to history
        self.add_message(conversation_id, "assistant", ai_response)

        return ai_response

    def clear_history(self, conversation_id: str):
        """Clear history for a conversation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM messages WHERE conversation_id = ?", (conversation_id,)
            )
            conn.commit()

    def get_conversation_ids(self) -> List[str]:
        """Get all conversation IDs"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT DISTINCT conversation_id FROM messages")
            return [row[0] for row in cursor.fetchall()]


# 3. PostgreSQL-based History Storage
class PostgresChatHistory:
    """Persistent conversation history using PostgreSQL"""

    def __init__(self, connection_string: str):
        """
        Initialize with PostgreSQL connection string
        Example: "postgresql://user:password@localhost:5432/chat_db"
        """
        try:
            import psycopg2

            self.psycopg2 = psycopg2
        except ImportError:
            raise ImportError(
                "psycopg2 is required for PostgreSQL support. Install with: pip install psycopg2-binary"
            )

        self.connection_string = connection_string
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        with self.psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        conversation_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            conn.commit()

    def add_message(self, conversation_id: str, role: str, content: str):
        """Add a message to conversation history"""
        with self.psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO messages (conversation_id, role, content) VALUES (%s, %s, %s)",
                    (conversation_id, role, content),
                )
            conn.commit()

    def get_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a specific conversation"""
        with self.psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT role, content FROM messages WHERE conversation_id = %s ORDER BY timestamp",
                    (conversation_id,),
                )
                return [
                    {"role": row[0], "content": row[1]} for row in cursor.fetchall()
                ]

    def chat(
        self, conversation_id: str, user_message: str, model: str = "llama3.2"
    ) -> str:
        """Send message and get AI response, updating history"""
        # Add user message to history
        self.add_message(conversation_id, "user", user_message)

        # Get current history
        history = self.get_history(conversation_id)

        # Get AI response
        ai_response = chat_with_history(history, model)

        # Add AI response to history
        self.add_message(conversation_id, "assistant", ai_response)

        return ai_response

    def clear_history(self, conversation_id: str):
        """Clear history for a conversation"""
        with self.psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM messages WHERE conversation_id = %s",
                    (conversation_id,),
                )
            conn.commit()

    def get_conversation_ids(self) -> List[str]:
        """Get all conversation IDs"""
        with self.psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT DISTINCT conversation_id FROM messages")
                return [row[0] for row in cursor.fetchall()]


# Usage Examples
if __name__ == "__main__":
    # Example 1: Runtime Dict
    print("=== Runtime Dict Example ===")
    runtime_history = RuntimeChatHistory()

    response1 = runtime_history.chat("conv1", "Hello, I'm Alice")
    print(f"AI: {response1}")

    response2 = runtime_history.chat("conv1", "What's my name?")
    print(f"AI: {response2}")

    print(f"History length: {len(runtime_history.get_history('conv1'))}")

    # Example 2: SQLite
    print("\n=== SQLite Example ===")
    sqlite_history = SQLiteChatHistory("example_chat.db")

    response3 = sqlite_history.chat("conv2", "Remember that I like pizza")
    print(f"AI: {response3}")

    response4 = sqlite_history.chat("conv2", "What food do I like?")
    print(f"AI: {response4}")

    print(f"Stored conversations: {sqlite_history.get_conversation_ids()}")

    # Example 3: PostgreSQL (commented out - requires PostgreSQL setup)
    print("\n=== PostgreSQL Example (requires setup) ===")
    # postgres_history = PostgresChatHistory("postgresql://user:pass@localhost/chat_db")
    # response5 = postgres_history.chat("conv3", "Hello from Postgres!")
    # print(f"AI: {response5}")

    print("\nAll examples completed successfully!")

