"""
Implement hybrid search combining keyword and semantic search
"""

import re

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


class HybridSearcher:
    """Combine keyword and semantic search for optimal retrieval"""

    def __init__(self, alpha: float = 0.5):
        """
        Args:
            alpha: Weight for semantic search (0-1)
                  0 = pure keyword, 1 = pure semantic
        """
        self.alpha = alpha

    def hybrid_search(
        self, query: str, documents: list[str], top_k: int = 5
    ) -> list[tuple[str, float]]:
        """Perform hybrid search combining BM25 and semantic similarity"""

        # Get keyword scores (simplified BM25)
        keyword_scores = self._bm25_search(query, documents)

        # Get semantic scores
        semantic_scores = self._semantic_search(query, documents)

        # Normalize scores to [0, 1]
        keyword_scores = self._normalize_scores(keyword_scores)
        semantic_scores = self._normalize_scores(semantic_scores)

        # Combine scores
        combined_scores = {}
        for doc in documents:
            kw_score = keyword_scores.get(doc, 0)
            sem_score = semantic_scores.get(doc, 0)

            # Weighted combination
            combined_scores[doc] = (1 - self.alpha) * kw_score + self.alpha * sem_score

        # Sort and return top results
        sorted_docs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_docs[:top_k]

    def _bm25_search(self, query: str, documents: list[str]) -> dict[str, float]:
        """Simplified BM25 keyword scoring"""
        from rank_bm25 import BM25Okapi

        # Tokenize documents
        tokenized_docs = [doc.lower().split() for doc in documents]
        bm25 = BM25Okapi(tokenized_docs)

        # Get scores for query
        query_tokens = query.lower().split()
        scores = bm25.get_scores(query_tokens)

        return dict(zip(documents, scores, strict=False))

    def _semantic_search(self, query: str, documents: list[str]) -> dict[str, float]:
        """Semantic similarity scoring using embeddings"""

        # Get embeddings for query and all documents at once (more efficient)
        all_texts = [query, *documents]
        embeddings = embedding_model.encode(all_texts, convert_to_numpy=True)

        query_emb = embeddings[0]
        doc_embeddings = embeddings[1:]

        scores = {}
        for doc, doc_emb in zip(documents, doc_embeddings, strict=False):
            # Calculate cosine similarity
            similarity = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
            )
            scores[doc] = float(similarity)

        return scores

    def _normalize_scores(self, scores: dict[str, float]) -> dict[str, float]:
        """Normalize scores to [0, 1] range"""
        if not scores:
            return {}

        min_score = min(scores.values())
        max_score = max(scores.values())

        if max_score == min_score:
            return dict.fromkeys(scores, 1.0)

        return {k: (v - min_score) / (max_score - min_score) for k, v in scores.items()}

    def adaptive_search(
        self, query: str, documents: list[str]
    ) -> list[tuple[str, float]]:
        """Automatically adjust search strategy based on query type"""

        # Detect query type and adjust alpha
        if self._is_specific_term(query):
            # Favor keyword search for specific terms
            self.alpha = 0.3
            search_type = "keyword-focused"
        elif self._is_conceptual(query):
            # Favor semantic search for concepts
            self.alpha = 0.8
            search_type = "semantic-focused"
        else:
            # Balanced approach
            self.alpha = 0.5
            search_type = "balanced"

        print(f"Query type detected: {search_type} (alpha={self.alpha})")

        return self.hybrid_search(query, documents)

    def _is_specific_term(self, query: str) -> bool:
        """Check if query contains specific terms/IDs"""
        patterns = [
            r"\b[A-Z]{2,}-\d+\b",  # ID patterns like USER-123
            r"\b\d{4,}\b",  # Long numbers
            r'"[^"]+"',  # Quoted terms
            r"\b[A-Z]{3,}\b",  # Acronyms
        ]
        return any(re.search(p, query) for p in patterns)

    def _is_conceptual(self, query: str) -> bool:
        """Check if query is conceptual/abstract"""
        conceptual_words = {
            "how",
            "why",
            "explain",
            "concept",
            "theory",
            "understanding",
            "relationship",
            "difference",
            "compare",
            "between",
            "impact",
            "effect",
        }
        query_words = set(query.lower().split())
        return bool(conceptual_words & query_words)


def demonstrate_hybrid_search():
    """Show hybrid search in action"""

    print("=== Hybrid Search Demo ===\n")

    # Sample document collection
    documents = [
        "USER-12345 encountered an authentication error at 10:30 AM when trying to access the admin panel.",
        "The authentication system uses OAuth 2.0 for secure user verification and token management.",
        "Error logs show multiple failed login attempts from IP address 192.168.1.100.",
        "Understanding authentication flows is crucial for implementing secure applications.",
        "Database query optimization can significantly improve application performance.",
        "USER-12345 reported slow query performance on the dashboard page.",
        "The relationship between caching and database performance is complex but important.",
        "SQL index strategies vary depending on query patterns and data distribution.",
        "Authentication tokens should be refreshed every 24 hours for security.",
        "Performance monitoring revealed bottlenecks in the authentication service.",
    ]

    # Test queries
    test_queries = [
        "USER-12345 error logs",  # Specific: should favor keyword
        "explain the relationship between caching and performance",  # Conceptual: should favor semantic
        "authentication security best practices",  # Balanced
        "SQL optimization",  # Technical but general
    ]

    searcher = HybridSearcher()

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 70)

        # Adaptive search
        results = searcher.adaptive_search(query, documents)

        print("\nTop Results:")
        for i, (doc, score) in enumerate(results[:3], 1):
            # Visual score bar
            bar_length = int(score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)

            print(f"\n{i}. Score: {score:.3f} [{bar}]")
            print(f"   {doc[:100]}..." if len(doc) > 100 else f"   {doc}")


def compare_search_methods():
    """Compare pure keyword vs pure semantic vs hybrid"""

    print("\n\n=== Search Method Comparison ===\n")

    documents = [
        "The car manufacturer recalled vehicles due to brake issues.",
        "Automobile companies must comply with safety regulations.",
        "Cars need regular oil changes for optimal performance.",
        "The cat jumped over the fence quickly.",
        "Vehicle maintenance is essential for longevity.",
        "Transportation safety standards are strictly enforced.",
        "The automotive industry is shifting towards electric vehicles.",
        "Cats are independent pets that require minimal care.",
    ]

    query = "car maintenance problems"

    print(f"Query: '{query}'")
    print("\nDocuments in collection:")
    for i, doc in enumerate(documents, 1):
        print(f"{i}. {doc}")

    # Test different approaches
    approaches = [
        ("Keyword Only", 0.0),
        ("Hybrid (Balanced)", 0.5),
        ("Semantic Only", 1.0),
    ]

    for approach_name, alpha in approaches:
        print(f"\n\n{approach_name} (alpha={alpha})")
        print("-" * 60)

        searcher = HybridSearcher(alpha=alpha)
        results = searcher.hybrid_search(query, documents, top_k=3)

        for i, (doc, score) in enumerate(results, 1):
            print(f"{i}. [{score:.3f}] {doc[:80]}...")


def demonstrate_reranking():
    """Show how reranking can improve results"""

    print("\n\n=== Reranking for Diversity (MMR) ===\n")

    documents = [
        "Python is a high-level programming language.",
        "Python programming is popular for data science.",
        "Python's syntax is clear and readable.",
        "Java is an object-oriented programming language.",
        "Machine learning models can be built with Python.",
        "Python libraries like NumPy are essential for numerical computing.",
        "JavaScript is primarily used for web development.",
        "Python frameworks like Django are great for web applications.",
    ]

    query = "Python programming"

    def mmr_rerank(
        query: str, documents: list[str], lambda_param: float = 0.7
    ) -> list[str]:
        """Maximal Marginal Relevance reranking for diversity"""

        # Get initial scores
        searcher = HybridSearcher(alpha=0.7)
        initial_results = searcher.hybrid_search(query, documents, top_k=len(documents))

        selected = []
        candidates = [doc for doc, _ in initial_results]
        scores = dict(initial_results)

        # Get embeddings for all documents at once (more efficient)
        doc_embeddings = embedding_model.encode(documents, convert_to_numpy=True)
        embeddings = dict(zip(documents, doc_embeddings, strict=False))

        while len(selected) < 5 and candidates:
            mmr_scores = {}

            for doc in candidates:
                # Relevance to query
                relevance = scores[doc]

                # Similarity to already selected docs
                if selected:
                    similarities = []
                    for selected_doc in selected:
                        sim = np.dot(embeddings[doc], embeddings[selected_doc]) / (
                            np.linalg.norm(embeddings[doc])
                            * np.linalg.norm(embeddings[selected_doc])
                        )
                        similarities.append(sim)
                    max_sim = max(similarities)
                else:
                    max_sim = 0

                # MMR score
                mmr_scores[doc] = (
                    lambda_param * relevance - (1 - lambda_param) * max_sim
                )

            # Select best document
            best_doc = max(mmr_scores, key=mmr_scores.get)
            selected.append(best_doc)
            candidates.remove(best_doc)

        return selected

    print(f"Query: '{query}'")

    # Standard ranking
    print("\nStandard Ranking (may have redundancy):")
    print("-" * 60)
    searcher = HybridSearcher(alpha=0.7)
    standard_results = searcher.hybrid_search(query, documents, top_k=5)

    for i, (doc, score) in enumerate(standard_results, 1):
        print(f"{i}. [{score:.3f}] {doc}")

    # MMR reranking
    print("\nMMR Reranking (promotes diversity):")
    print("-" * 60)
    diverse_results = mmr_rerank(query, documents, lambda_param=0.7)

    for i, doc in enumerate(diverse_results, 1):
        print(f"{i}. {doc}")


def main():
    """Run all hybrid search demonstrations"""
    demonstrate_hybrid_search()
    compare_search_methods()
    demonstrate_reranking()


if __name__ == "__main__":
    main()
