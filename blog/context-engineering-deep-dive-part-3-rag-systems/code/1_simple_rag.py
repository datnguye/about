"""
Simple RAG implementation using DuckDB vector similarity search and sentence-transformers
"""

import os

import duckdb
from dotenv import load_dotenv
from litellm import completion
from sentence_transformers import SentenceTransformer

load_dotenv()


class SimpleRAG:
    def __init__(self, db_path: str = ":memory:"):
        """Initialize a simple RAG system with DuckDB"""
        self.conn = duckdb.connect(db_path)

        # Install and load the VSS extension for vector similarity search
        self.conn.execute("INSTALL vss")
        self.conn.execute("LOAD vss")

        # Initialize sentence transformer model (lightweight model)
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embedding_dim = 384  # Dimension of all-MiniLM-L6-v2

        # Create the documents table with vector column
        self.conn.execute(f"""
            CREATE SEQUENCE doc_id_seq;
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY DEFAULT nextval('doc_id_seq'),
                content TEXT,
                embedding FLOAT[{self.embedding_dim}],
                metadata JSON
            )
        """)

        print("RAG system initialized with DuckDB vector search")

    def add_documents(self, documents: list[str], metadata: list[dict] | None = None):
        """Add documents to the vector store"""
        print(f"Generating embeddings for {len(documents)} documents...")

        # Generate embeddings using sentence-transformers
        embeddings = self.embedding_model.encode(documents, convert_to_numpy=True)

        # Prepare metadata
        if metadata is None:
            metadata = [{"source": "demo"} for _ in documents]

        # Insert documents with embeddings
        for _i, (doc, embedding, meta) in enumerate(
            zip(documents, embeddings, metadata, strict=False)
        ):
            self.conn.execute(
                """
                INSERT INTO documents (content, embedding, metadata)
                VALUES (?, ?, ?)
            """,
                [doc, embedding.tolist(), meta],
            )

        print(f"Added {len(documents)} documents to the vector store")

    def query(self, question: str, n_results: int = 3) -> str:
        """Query the RAG system"""
        # Step 1: Generate embedding for the question
        print(f"Generating embedding for question: '{question}'")
        query_embedding = self.embedding_model.encode(
            [question], convert_to_numpy=True
        )[0]

        # Step 2: Perform vector similarity search using DuckDB VSS
        results = self.conn.execute(
            f"""
            SELECT
                content,
                array_cosine_similarity(embedding, $1::FLOAT[{self.embedding_dim}]) as similarity,
                metadata
            FROM documents
            ORDER BY similarity DESC
            LIMIT {n_results}
        """,
            [query_embedding.tolist()],
        ).fetchall()

        if not results:
            return "No relevant documents found."

        # Step 3: Build context from retrieved documents
        context_parts = []
        print(f"Retrieved {len(results)} relevant documents:")
        for i, (content, similarity, _metadata) in enumerate(results, 1):
            print(f"  {i}. Similarity: {similarity:.3f} - {content[:100]}...")
            context_parts.append(content)

        context = "\n\n".join(context_parts)

        # Step 4: Generate answer using LLM with context
        try:
            response = completion(
                model="openrouter/openai/gpt-oss-20b:free",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                messages=[
                    {
                        "role": "system",
                        "content": "Answer questions based on the provided context. Be concise and specific. If the answer isn't in the context, say so clearly.",
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:",
                    },
                ],
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"LLM error: {e}")
            # Fallback: return the most relevant document excerpt
            return f"Based on the most relevant document: {results[0][0][:200]}..."


def main():
    """Demo the RAG system"""
    print("=== Simple RAG System Demo with DuckDB ===\n")

    # Initialize RAG
    rag = SimpleRAG()

    # Sample company documents
    company_docs = [
        "Our refund policy for enterprise customers: 90-day refund window with manager approval required. Standard customers have 30-day refund policy.",
        "Support SLA for enterprise: 1-hour response time, 4-hour resolution for critical issues.",
        "Standard support offers 24-hour response time and best-effort resolution.",
        "Premium tier includes 24/7 phone support, dedicated account manager, and custom integrations.",
        "Enterprise customers get priority handling for all refund requests and technical support issues.",
        "All refunds must be requested through the customer portal with order number and reason.",
    ]

    # Add documents to RAG
    rag.add_documents(company_docs)

    print("\n=== Testing RAG Queries ===\n")

    # Test queries
    test_queries = [
        "What's the refund window for enterprise clients?",
        "How quickly do enterprise customers get support?",
        "What are the benefits of premium tier?",
    ]

    for query in test_queries:
        print(f"Q: {query}")
        answer = rag.query(query)
        print(f"A: {answer}")
        print("-" * 50)


if __name__ == "__main__":
    main()
