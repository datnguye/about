from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from datetime import datetime


class SemanticMemory:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.encoder = SentenceTransformer(model_name)
        self.memories: List[Dict] = []
        self.embeddings: List[np.ndarray] = []

    def store_memory(self, content: str, metadata: Dict = None) -> str:
        """Store content with semantic embedding"""
        memory_id = f"mem_{len(self.memories)}_{int(datetime.now().timestamp())}"

        # Generate embedding
        embedding = self.encoder.encode(content)

        # Store memory
        memory = {
            "id": memory_id,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "access_count": 0,
        }

        self.memories.append(memory)
        self.embeddings.append(embedding)

        return memory_id

    def retrieve_similar(
        self, query: str, top_k: int = 5, threshold: float = 0.7
    ) -> List[Dict]:
        """Find semantically similar memories"""
        if not self.embeddings:
            return []

        # Encode query
        query_embedding = self.encoder.encode(query)

        # Calculate similarities
        similarities = []
        for i, memory_embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, memory_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
            )
            similarities.append((i, similarity))

        # Sort by similarity and filter by threshold
        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in similarities[:top_k]:
            if score >= threshold:
                memory = self.memories[idx].copy()
                memory["similarity_score"] = float(score)
                # Update access count
                self.memories[idx]["access_count"] += 1
                results.append(memory)

        return results

    def get_memory_clusters(self, n_clusters: int = 3) -> Dict:
        """Group similar memories into clusters"""
        if len(self.embeddings) < n_clusters:
            return {"clusters": [], "message": "Not enough memories for clustering"}

        from sklearn.cluster import KMeans

        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(self.embeddings)

        # Group memories by cluster
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append({"memory": self.memories[i], "embedding_idx": i})

        # Calculate cluster summaries
        cluster_summaries = []
        for label, cluster_memories in clusters.items():
            contents = [mem["memory"]["content"] for mem in cluster_memories]
            cluster_summaries.append(
                {
                    "cluster_id": label,
                    "size": len(cluster_memories),
                    "memories": cluster_memories,
                    "sample_content": contents[0] if contents else "",
                }
            )

        return {"clusters": cluster_summaries}


def demo_semantic_memory():
    print("=== Semantic Memory Demo ===")
    semantic_memory = SemanticMemory()

    # Store various types of memories
    memories_to_store = [
        (
            "User prefers concise code examples with comments",
            {"type": "preference", "importance": 0.9},
        ),
        (
            "Customer uses PostgreSQL 14 with Django ORM",
            {"type": "technical_context", "importance": 0.8},
        ),
        (
            "Debugging session: login timeout issues resolved by increasing session timeout",
            {"type": "solution", "importance": 0.9},
        ),
        (
            "User wants cost-effective solutions, mentioned budget constraints",
            {"type": "preference", "importance": 0.7},
        ),
        (
            "Fixed database connection pooling issue in production",
            {"type": "solution", "importance": 0.8},
        ),
        (
            "User asked about Python best practices for web development",
            {"type": "query", "importance": 0.6},
        ),
        (
            "Resolved memory leak in Django application by optimizing queryset",
            {"type": "solution", "importance": 0.9},
        ),
        (
            "Customer prefers AWS over Google Cloud for deployment",
            {"type": "preference", "importance": 0.7},
        ),
        (
            "Implemented caching strategy using Redis for better performance",
            {"type": "solution", "importance": 0.8},
        ),
        (
            "User mentioned they work with large datasets and need efficient processing",
            {"type": "context", "importance": 0.8},
        ),
    ]

    print("Storing memories...")
    for content, metadata in memories_to_store:
        memory_id = semantic_memory.store_memory(content, metadata)
        print(f"✓ Stored: {memory_id[:12]}... - {content[:50]}...")

    print(f"\nTotal memories stored: {len(semantic_memory.memories)}")
    print()

    # Test semantic retrieval with different queries
    test_queries = [
        "Show me efficient database code",
        "What are the user's preferences?",
        "Help with performance optimization",
        "Cloud deployment options",
        "Python web development advice",
    ]

    print("=== Semantic Retrieval Tests ===")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        relevant = semantic_memory.retrieve_similar(query, top_k=3, threshold=0.3)

        if relevant:
            print("Relevant memories:")
            for i, memory in enumerate(relevant):
                score = memory["similarity_score"]
                content = memory["content"]
                memory_type = memory["metadata"].get("type", "unknown")
                importance = memory["metadata"].get("importance", 0)

                print(f"  {i + 1}. [{memory_type}] {content}")
                print(
                    f"     Similarity: {score:.3f}, Importance: {importance}, Accessed: {memory['access_count']} times"
                )
        else:
            print("No relevant memories found above threshold")

    print("\n=== Memory Clustering Analysis ===")
    clusters = semantic_memory.get_memory_clusters(n_clusters=3)

    if "clusters" in clusters:
        for cluster in clusters["clusters"]:
            print(f"\nCluster {cluster['cluster_id']} ({cluster['size']} memories):")
            print(f"Sample: {cluster['sample_content'][:80]}...")

            # Show cluster composition by type
            types = {}
            for mem_data in cluster["memories"]:
                mem_type = mem_data["memory"]["metadata"].get("type", "unknown")
                types[mem_type] = types.get(mem_type, 0) + 1

            print(f"Types: {dict(types)}")

    print("\n=== Memory Access Patterns ===")
    access_stats = {}
    for memory in semantic_memory.memories:
        memory_type = memory["metadata"].get("type", "unknown")
        access_count = memory["access_count"]

        if memory_type not in access_stats:
            access_stats[memory_type] = {"total_accesses": 0, "count": 0}

        access_stats[memory_type]["total_accesses"] += access_count
        access_stats[memory_type]["count"] += 1

    for mem_type, stats in access_stats.items():
        avg_access = (
            stats["total_accesses"] / stats["count"] if stats["count"] > 0 else 0
        )
        print(f"- {mem_type}: {stats['count']} memories, avg {avg_access:.1f} accesses")

    return semantic_memory


if __name__ == "__main__":
    demo_semantic_memory()
