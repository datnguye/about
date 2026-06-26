from typing import Dict, List
from datetime import datetime


# Simplified versions of the memory components for this example
class ConversationMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        # Keep only last 10 messages for demo
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]

    def get_context(self) -> List[Dict]:
        return self.messages.copy()


class SemanticMemory:
    def __init__(self):
        self.memories = []

    def store_memory(self, content: str, metadata: Dict = None):
        memory = {
            "content": content,
            "metadata": metadata or {},
            "stored_at": datetime.now().isoformat(),
        }
        self.memories.append(memory)
        return f"mem_{len(self.memories)}"

    def retrieve_similar(self, query: str, top_k: int = 3) -> List[Dict]:
        # Simplified similarity: just check if query words appear in memory
        results = []
        query_words = set(query.lower().split())

        for memory in self.memories:
            content_words = set(memory["content"].lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                memory_copy = memory.copy()
                memory_copy["similarity_score"] = overlap / len(query_words)
                results.append(memory_copy)

        # Sort by similarity and return top_k
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:top_k]


class HybridMemorySystem:
    """
    Three-tier memory architecture:
    - Hot Memory (Redis): Fast access, temporary storage
    - Warm Memory (In-Memory): Session state, conversation context
    - Cold Memory (Vector Store): Long-term semantic storage
    """

    def __init__(self):
        # For demo purposes, we'll simulate Redis with a dict
        # In production, use: redis.from_url("redis://localhost:6379")
        self.hot_memory = {}  # Simulated Redis
        self.warm_memory = ConversationMemory()  # Session state
        self.cold_memory = SemanticMemory()  # Long-term storage

    def store_interaction(self, user_id: str, interaction: Dict) -> None:
        """Store interaction across all three memory tiers"""
        print(f"Storing interaction for user {user_id}")

        # Always store in hot memory (fast, temporary)
        self.hot_memory[f"recent:{user_id}"] = {
            "data": interaction,
            "expires_at": datetime.now().timestamp() + 3600,  # 1 hour TTL
        }
        print(f"✓ Stored in hot memory (Redis): {interaction['content'][:50]}...")

        # Update warm memory (session context)
        self.warm_memory.add_message(interaction["role"], interaction["content"])
        print(
            f"✓ Updated warm memory (session): {len(self.warm_memory.messages)} messages"
        )

        # Selectively store in cold memory (expensive, permanent)
        importance = self._calculate_importance(interaction)
        print(f"✓ Calculated importance score: {importance}")

        if importance > 0.7:  # Only important stuff goes to long-term
            memory_id = self.cold_memory.store_memory(
                interaction["content"],
                metadata={"user_id": user_id, "importance": importance},
            )
            print(f"✓ Stored in cold memory (vector): {memory_id}")
        else:
            print("✗ Not important enough for long-term storage")

    def _calculate_importance(self, interaction: Dict) -> float:
        """Calculate importance score for an interaction"""
        score = 0.5  # Base score
        content = interaction.get("content", "").lower()

        # Boost for problem-solving keywords
        if any(
            word in content for word in ["error", "bug", "issue", "problem", "help"]
        ):
            score += 0.2

        # Boost for code or technical content
        if any(
            word in content
            for word in ["code", "function", "class", "import", "database"]
        ):
            score += 0.1

        # Boost for user preferences
        if any(word in content for word in ["prefer", "like", "want", "need"]):
            score += 0.3

        return min(score, 1.0)

    def get_context(self, user_id: str, query: str) -> Dict:
        """Retrieve relevant context from all memory systems"""
        print(f"\nRetrieving context for user {user_id}, query: '{query}'")

        # Get from hot memory (recent interactions)
        recent_key = f"recent:{user_id}"
        recent = self.hot_memory.get(recent_key, {}).get("data", {})

        # Get from warm memory (conversation history)
        conversation = self.warm_memory.get_context()

        # Get from cold memory (semantic similarity)
        similar_past = self.cold_memory.retrieve_similar(query, top_k=3)

        context = {
            "recent": recent,
            "conversation": conversation,
            "similar_past": similar_past,
        }

        print("✓ Context assembled:")
        print(f"  - Recent: {'Yes' if recent else 'No'}")
        print(f"  - Conversation: {len(conversation)} messages")
        print(f"  - Similar past: {len(similar_past)} memories")

        return context


def main():
    """Demonstrate the hybrid memory system"""
    print("=== Hybrid Memory System Demo ===\n")

    # Initialize the system
    memory_system = HybridMemorySystem()
    user_id = "user_123"

    # Simulate a series of interactions
    interactions = [
        {
            "role": "user",
            "content": "I'm getting a database timeout error in my Python app",
            "timestamp": datetime.now().isoformat(),
        },
        {
            "role": "assistant",
            "content": "Let's debug this step by step. First, check your connection pool settings.",
            "timestamp": datetime.now().isoformat(),
        },
        {
            "role": "user",
            "content": "I prefer concise code examples with detailed comments",
            "timestamp": datetime.now().isoformat(),
        },
        {
            "role": "assistant",
            "content": "I'll keep that in mind. Here's a concise example with explanatory comments.",
            "timestamp": datetime.now().isoformat(),
        },
        {
            "role": "user",
            "content": "What's the weather like?",
            "timestamp": datetime.now().isoformat(),
        },
    ]

    # Store each interaction
    for i, interaction in enumerate(interactions):
        print(f"\n--- Interaction {i + 1} ---")
        memory_system.store_interaction(user_id, interaction)

    # Retrieve context for a new query
    print("\n" + "=" * 50)
    query = "Show me how to optimize database connections"
    context = memory_system.get_context(user_id, query)

    print("\n=== Final Context Summary ===")
    print(f"Query: '{query}'")
    print(f"Hot Memory: {bool(context['recent'])}")
    print(f"Warm Memory: {len(context['conversation'])} messages")
    print(f"Cold Memory: {len(context['similar_past'])} relevant memories")

    if context["similar_past"]:
        print("\nMost relevant past memory:")
        best_match = context["similar_past"][0]
        print(f"  Content: {best_match['content'][:100]}...")
        print(f"  Similarity: {best_match['similarity_score']:.2f}")


if __name__ == "__main__":
    main()
