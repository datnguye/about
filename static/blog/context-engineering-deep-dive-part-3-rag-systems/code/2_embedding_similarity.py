"""
Demonstrate semantic similarity with text embeddings
"""

import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

# Initialize the embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts"""

    # Convert texts to vectors using sentence-transformers
    embeddings = embedding_model.encode([text1, text2], convert_to_numpy=True)
    embed1, embed2 = embeddings[0], embeddings[1]

    # Calculate cosine similarity
    similarity = np.dot(embed1, embed2) / (
        np.linalg.norm(embed1) * np.linalg.norm(embed2)
    )

    return similarity


def compare_embeddings_demo():
    """Show how different text pairs have different similarities"""

    print("=== Semantic Similarity Demo ===\n")

    # Test pairs with varying semantic similarity
    examples = [
        ("The cat sat on the mat", "A feline rested on the rug"),  # Same meaning
        ("The cat sat on the mat", "Dogs love to play fetch"),  # Different topic
        ("SELECT * FROM users", "Get all user records"),  # Technical similarity
        ("bug", "defect"),  # Synonyms
        ("bug", "insect"),  # Different context
        ("python code", "snake behavior"),  # Same word, different meaning
        ("Machine learning model", "AI algorithm"),  # Related concepts
        ("Database query optimization", "SQL performance tuning"),  # Technical synonyms
    ]

    print("Comparing text pairs for semantic similarity:")
    print("(1.0 = identical meaning, 0.0 = completely unrelated)\n")
    print("-" * 80)

    for text1, text2 in examples:
        score = semantic_similarity(text1, text2)

        # Visual representation of similarity
        bar_length = int(score * 30)
        bar = "█" * bar_length + "░" * (30 - bar_length)

        print(f"Similarity: {score:.3f} [{bar}]")
        print(f"Text 1: '{text1}'")
        print(f"Text 2: '{text2}'")
        print("-" * 80)


def find_most_similar():
    """Find the most similar text from a collection"""

    print("\n=== Finding Most Similar Text ===\n")

    # Collection of technical documents
    documents = [
        "How to optimize database queries for better performance",
        "Best practices for machine learning model training",
        "Setting up a React application with TypeScript",
        "Understanding SQL indexes and query optimization",
        "Deep learning fundamentals and neural networks",
        "Building REST APIs with Node.js and Express",
        "Database performance tuning and index strategies",
        "Introduction to natural language processing",
    ]

    query = "improving slow SQL queries"

    print(f"Query: '{query}'\n")
    print("Searching through documents...\n")

    # Calculate similarities
    similarities = []
    for doc in documents:
        score = semantic_similarity(query, doc)
        similarities.append((doc, score))

    # Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Show results
    print("Documents ranked by relevance:\n")
    for i, (doc, score) in enumerate(similarities, 1):
        relevance = "⭐" * min(5, int(score * 10))  # Visual stars
        print(f"{i}. [{score:.3f}] {relevance}")
        print(f"   {doc}\n")


def embedding_dimensions_demo():
    """Show the structure of embeddings"""

    print("\n=== Embedding Structure ===\n")

    sample_text = "Understanding embeddings in RAG systems"

    # Get embedding using sentence-transformers
    embed_vector = embedding_model.encode([sample_text], convert_to_numpy=True)[0]

    print(f"Text: '{sample_text}'")
    print(f"Embedding dimensions: {len(embed_vector)}")
    print(f"Vector type: {type(embed_vector)}")
    print(f"First 10 values: {embed_vector[:10]}")
    print(f"Value range: [{min(embed_vector):.3f}, {max(embed_vector):.3f}]")
    print(f"Mean value: {np.mean(embed_vector):.3f}")
    print(f"Std deviation: {np.std(embed_vector):.3f}")


def main():
    """Run all embedding demonstrations"""
    compare_embeddings_demo()
    find_most_similar()
    embedding_dimensions_demo()


if __name__ == "__main__":
    main()
