"""
Demonstrate hybrid search: combining keyword and semantic search
"""

import re

import numpy as np
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def has_specific_terms(query: str) -> bool:
    """Check if query contains specific terms like IDs or codes"""
    patterns = [
        r"\b[A-Z]{2,}-\d+\b",  # ID patterns like USER-123, ORDER-456
        r"\b\d{6,}\b",  # Long numbers
        r'"[^"]+"',  # Quoted exact terms
        r"\b[A-Z]{3,}\b",  # Acronyms like SQL, API
    ]
    return any(re.search(p, query) for p in patterns)


def is_conceptual(query: str) -> bool:
    """Check if query is asking for explanations or concepts"""
    conceptual_words = {
        "explain",
        "how",
        "why",
        "what",
        "understanding",
        "concept",
        "theory",
    }
    query_words = set(query.lower().split())
    return bool(conceptual_words & query_words)


def bm25_search(query: str, documents: list[str]) -> dict[str, float]:
    """BM25 keyword search using rank-bm25 library"""
    # Tokenize documents
    tokenized_docs = [doc.lower().split() for doc in documents]

    # Initialize BM25
    bm25 = BM25Okapi(tokenized_docs)

    # Tokenize query
    query_tokens = query.lower().split()

    # Get BM25 scores
    doc_scores = bm25.get_scores(query_tokens)

    # Create scores dictionary
    scores = {
        doc: float(score) for doc, score in zip(documents, doc_scores, strict=False)
    }

    return scores


def vector_search(query: str, documents: list[str]) -> dict[str, float]:
    """Semantic search using embeddings and cosine similarity"""
    # Get embeddings for query and documents
    all_texts = [query, *documents]
    embeddings = model.encode(all_texts, convert_to_numpy=True)

    query_emb = embeddings[0]
    doc_embeddings = embeddings[1:]

    scores = {}
    for doc, doc_emb in zip(documents, doc_embeddings, strict=False):
        # Cosine similarity
        similarity = np.dot(query_emb, doc_emb) / (
            np.linalg.norm(query_emb) * np.linalg.norm(doc_emb)
        )
        scores[doc] = float(similarity)

    return scores


def combine_scores(
    keyword_scores: dict[str, float], semantic_scores: dict[str, float], alpha: float
) -> list[tuple[str, float]]:
    """Combine keyword and semantic scores with given weight"""

    # Normalize scores to [0, 1]
    def normalize(scores):
        if not scores:
            return {}
        min_val = min(scores.values())
        max_val = max(scores.values())
        if max_val == min_val:
            return dict.fromkeys(scores, 1.0)
        return {k: (v - min_val) / (max_val - min_val) for k, v in scores.items()}

    keyword_norm = normalize(keyword_scores)
    semantic_norm = normalize(semantic_scores)

    # Combine with alpha weight
    combined = {}
    for doc in keyword_scores:
        kw_score = keyword_norm.get(doc, 0)
        sem_score = semantic_norm.get(doc, 0)
        combined[doc] = (1 - alpha) * kw_score + alpha * sem_score

    # Sort by score
    return sorted(combined.items(), key=lambda x: x[1], reverse=True)


def hybrid_search(
    query: str, documents: list[str], alpha: float = 0.5
) -> list[tuple[str, float]]:
    """
    Hybrid search combining keyword and semantic search.

    Args:
        query: Search query
        documents: List of documents to search
        alpha: Weight for semantic search (0=keyword only, 1=semantic only)

    Returns:
        Sorted list of (document, score) tuples
    """
    # Auto-adjust alpha based on query type
    if has_specific_terms(query):  # IDs, codes
        alpha = 0.3  # Favor keyword
        print(f"  → Detected specific terms, using alpha={alpha} (keyword-focused)")
    elif is_conceptual(query):  # "explain", "how"
        alpha = 0.8  # Favor semantic
        print(f"  → Detected conceptual query, using alpha={alpha} (semantic-focused)")
    else:
        print(f"  → Using balanced search, alpha={alpha}")

    keyword_scores = bm25_search(query, documents)
    semantic_scores = vector_search(query, documents)
    return combine_scores(keyword_scores, semantic_scores, alpha)


def main():
    """Demonstrate hybrid search with different query types"""

    # Sample documents
    documents = [
        "USER-12345 encountered authentication error at 10:30 AM",
        "The authentication system uses OAuth 2.0 for secure verification",
        "Error code AUTH-500 indicates server-side authentication failure",
        "Understanding how authentication works is crucial for security",
        "Database query optimization improves application performance",
        "ORDER-67890 was processed successfully at 11:45 AM",
        "Explain the relationship between caching and database performance",
        "API-KEY-789 expired and needs renewal",
    ]

    # Test queries showing different search behaviors
    test_queries = [
        "USER-12345 error",  # Specific ID - should favor keyword
        "explain authentication security",  # Conceptual - should favor semantic
        "authentication OAuth",  # Balanced - mix of both
        "ORDER-67890",  # Very specific - strong keyword bias
        "how does caching work",  # Very conceptual - strong semantic bias
    ]

    print("=" * 70)
    print("HYBRID SEARCH DEMONSTRATION")
    print("=" * 70)
    print("\nDocuments in collection:")
    for i, doc in enumerate(documents, 1):
        print(f"{i}. {doc}")

    print("\n" + "=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 50)

        results = hybrid_search(query, documents)

        # Show top 3 results
        print("\nTop 3 Results:")
        for i, (doc, score) in enumerate(results[:3], 1):
            # Visual score bar
            bar_length = int(score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"\n  {i}. [{bar}] Score: {score:.3f}")
            print(f"     {doc}")

    # Demonstrate manual alpha control
    print("\n" + "=" * 70)
    print("MANUAL ALPHA CONTROL COMPARISON")
    print("=" * 70)

    query = "authentication system security"
    print(f"\n🔍 Query: '{query}'")

    for alpha_name, alpha_value in [
        ("Keyword-only", 0.0),
        ("Balanced", 0.5),
        ("Semantic-only", 1.0),
    ]:
        print(f"\n{alpha_name} (alpha={alpha_value}):")
        print("-" * 30)

        keyword_scores = bm25_search(query, documents)
        semantic_scores = vector_search(query, documents)
        results = combine_scores(keyword_scores, semantic_scores, alpha_value)

        for i, (doc, score) in enumerate(results[:2], 1):
            print(f"  {i}. [{score:.3f}] {doc[:60]}...")


if __name__ == "__main__":
    main()
