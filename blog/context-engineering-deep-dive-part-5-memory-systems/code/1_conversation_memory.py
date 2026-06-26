from litellm import completion
from typing import List, Dict
import tiktoken
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class ConversationMemory:
    def __init__(self, max_tokens: int = 2000, model: str = "gpt-3.5-turbo"):
        self.messages: List[Dict] = []
        self.max_tokens = max_tokens
        self.encoder = tiktoken.encoding_for_model(model)

    def add_message(self, role: str, content: str) -> None:
        """Add message and trim if needed"""
        self.messages.append({"role": role, "content": content})
        self._smart_trim()

    def _smart_trim(self) -> None:
        """Keep system prompt + recent messages within token limit"""
        while self._count_tokens() > self.max_tokens and len(self.messages) > 2:
            # Never remove system prompt (index 0) or last message
            # Remove from the middle, preserving conversation flow
            if len(self.messages) > 3:
                # Remove oldest user/assistant pair
                self.messages.pop(1)  # Remove old user message
                if len(self.messages) > 2:
                    self.messages.pop(1)  # Remove old assistant response

    def _count_tokens(self) -> int:
        """Count total tokens in conversation"""
        total = 0
        for message in self.messages:
            total += len(self.encoder.encode(message["content"]))
        return total

    def get_context(self) -> List[Dict]:
        """Get trimmed conversation for LLM"""
        return self.messages.copy()


def demo_conversation_memory():
    # Initialize memory with token limit
    memory = ConversationMemory(max_tokens=1000)

    # Add system prompt
    memory.add_message(
        "system", "You are a helpful coding assistant specializing in Python."
    )

    # Simulate a long conversation
    conversation_pairs = [
        (
            "Help me debug this Python function",
            "I'd be happy to help! Please share the function code.",
        ),
        (
            "def calculate_sum(numbers): return sum(numbers)",
            "That function looks correct! It calculates the sum of numbers in a list.",
        ),
        (
            "It's giving me a TypeError",
            "The TypeError suggests you might be passing incompatible types. What error message do you see?",
        ),
        (
            "TypeError: unsupported operand type(s) for +: 'int' and 'str'",
            "Ah! You have strings mixed with integers. Try converting strings to integers first.",
        ),
        (
            "How do I convert strings to integers?",
            "Use int() function: int('5') converts string '5' to integer 5.",
        ),
        (
            "What about handling non-numeric strings?",
            "Use try/except with ValueError: try: int(x) except ValueError: handle error",
        ),
        (
            "Show me a complete example",
            "Here's a robust version with error handling...",
        ),
    ]

    print("=== Conversation Memory Demo ===")
    print(f"Token limit: {memory.max_tokens}")
    print()

    for i, (user_msg, assistant_msg) in enumerate(conversation_pairs):
        print(f"--- Turn {i + 1} ---")

        # Add messages
        memory.add_message("user", user_msg)
        memory.add_message("assistant", assistant_msg)

        # Show current state
        token_count = memory._count_tokens()
        message_count = len(memory.messages)

        print(f"Messages: {message_count}, Tokens: {token_count}")

        if token_count > memory.max_tokens * 0.8:  # Warn when approaching limit
            print("⚠️  Approaching token limit - older messages will be trimmed")

        print()

    print("=== Final Context ===")
    context = memory.get_context()
    for i, msg in enumerate(context):
        role_emoji = (
            "🤖"
            if msg["role"] == "assistant"
            else "👤"
            if msg["role"] == "user"
            else "⚙️"
        )
        content_preview = (
            msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]
        )
        print(f"{i + 1}. {role_emoji} {msg['role']}: {content_preview}")

    print(f"\nFinal token count: {memory._count_tokens()}")
    return context


def test_with_llm(context):
    """Test the conversation memory with actual LLM"""
    try:
        # Add a new user message to test context retention
        test_context = context + [
            {
                "role": "user",
                "content": "Can you remind me what we were discussing about error handling?",
            }
        ]

        response = completion(
            model="openrouter/openai/gpt-oss-20b:free",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=test_context,
            temperature=0.3,
        )

        print("=== LLM Response Test ===")
        print("Query: Can you remind me what we were discussing about error handling?")
        print(f"Response: {response['choices'][0]['message']['content']}")

    except Exception as e:
        print(f"LLM test failed: {e}")
        print("Make sure you have OPENROUTER_API_KEY set in your .env file")


if __name__ == "__main__":
    context = demo_conversation_memory()
    print("\n" + "=" * 50 + "\n")
    test_with_llm(context)
