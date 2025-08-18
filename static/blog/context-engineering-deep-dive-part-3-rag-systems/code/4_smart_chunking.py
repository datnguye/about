"""
Smart chunking strategies using LangChain Text Splitters
"""

import numpy as np
from dotenv import load_dotenv
from langchain_text_splitters import (
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    PythonCodeTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from sentence_transformers import SentenceTransformer

load_dotenv()


class SmartChunker:
    """Demonstrate LangChain text splitters for RAG systems"""

    def __init__(self):
        """Initialize different chunking strategies"""
        print("SmartChunker initialized with LangChain text splitters")

        # Initialize embedding model for semantic chunking simulation
        try:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
            print("✅ Embedding model available for semantic chunking")
            self.semantic_available = True
        except Exception as e:
            print(f"⚠️  Embedding model initialization failed: {e}")
            self.semantic_available = False

    def fixed_size_chunk(
        self, text: str, chunk_size: int = 500, overlap: int = 50
    ) -> list[str]:
        """
        Fixed-size chunking using CharacterTextSplitter
        Pros: Simple, uniform sizes, fast
        Cons: Breaks sentences, ignores document structure
        """
        splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            separator="\n\n",  # Split on double newlines first
        )

        chunks = splitter.split_text(text)
        return chunks

    def content_aware_chunk(self, text: str, doc_type: str = "general") -> list[str]:
        """
        Content-aware chunking using RecursiveCharacterTextSplitter
        Pros: Respects document structure, preserves meaning
        Cons: Variable chunk sizes, more complex
        """
        if doc_type == "code":
            # Use Python-specific code splitter
            splitter = PythonCodeTextSplitter(chunk_size=1500, chunk_overlap=200)
        elif doc_type == "markdown":
            # Use markdown header splitter for structure-aware splitting
            headers_to_split_on = [
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ]
            markdown_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on
            )

            # First split by headers, then by size
            md_docs = markdown_splitter.split_text(text)

            # Then split large sections further
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )

            chunks = []
            for doc in md_docs:
                sub_chunks = text_splitter.split_text(doc.page_content)
                chunks.extend(sub_chunks)
            return chunks

        elif doc_type == "legal":
            # Larger chunks for legal documents to preserve context
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=300,
                separators=[
                    "\n\n## ",
                    "\n\n### ",
                    "\n\nSection ",
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    "",
                ],
            )
        else:
            # General recursive text splitter - most commonly used
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", ". ", " ", ""],  # Try these in order
            )

        chunks = splitter.split_text(text)
        return chunks

    def semantic_chunk(self, text: str) -> list[str]:
        """
        Semantic chunking using sentence similarity approach
        Pros: Best content coherence, meaning preservation
        Cons: Computationally expensive, requires embeddings
        """
        if not self.semantic_available:
            print("Semantic chunking not available, falling back to content-aware")
            return self.content_aware_chunk(text)

        try:
            # Split into sentences first
            sentences = self._split_into_sentences(text)
            if len(sentences) <= 1:
                return [text]

            # Get embeddings for all sentences
            embeddings = self.embedding_model.encode(sentences, convert_to_numpy=True)

            # Group sentences by similarity
            chunks = []
            current_chunk = [sentences[0]]
            current_length = len(sentences[0])
            target_length = 800  # Target chunk size

            for i in range(1, len(sentences)):
                sentence = sentences[i]
                sentence_length = len(sentence)

                # Calculate similarity with current chunk (use last sentence as representative)
                similarity = np.dot(embeddings[i - 1], embeddings[i]) / (
                    np.linalg.norm(embeddings[i - 1]) * np.linalg.norm(embeddings[i])
                )

                # Decide whether to continue current chunk or start new one
                if (
                    current_length + sentence_length <= target_length
                    and similarity > 0.5
                ):  # High similarity threshold
                    current_chunk.append(sentence)
                    current_length += sentence_length
                else:
                    # Start new chunk
                    if current_chunk:
                        chunks.append(" ".join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length

            # Add final chunk
            if current_chunk:
                chunks.append(" ".join(current_chunk))

            return chunks

        except Exception as e:
            print(f"Semantic chunking failed: {e}, using fallback")
            return self.content_aware_chunk(text)

    def _split_into_sentences(self, text: str) -> list[str]:
        """Split text into sentences"""
        import re

        # Simple sentence splitting (in practice, use NLTK or spaCy)
        sentence_endings = r"[.!?]+(?:\s|$)"
        sentences = re.split(sentence_endings, text)
        return [s.strip() for s in sentences if s.strip()]

    def token_based_chunk(self, text: str, chunk_size: int = 400) -> list[str]:
        """
        Token-based chunking using TokenTextSplitter
        Useful when you need precise token control for LLM context windows
        """
        splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=50)

        chunks = splitter.split_text(text)
        return chunks

    def chunk_by_type(
        self, text: str, doc_type: str, strategy: str = "content_aware"
    ) -> list[str]:
        """Choose chunking strategy based on document type and strategy"""

        print(f"Chunking {doc_type} document using {strategy} strategy")

        if strategy == "fixed_size":
            return self.fixed_size_chunk(text)
        elif strategy == "semantic":
            return self.semantic_chunk(text)
        elif strategy == "token_based":
            return self.token_based_chunk(text)
        else:  # content_aware (default)
            return self.content_aware_chunk(text, doc_type)


def demonstrate_chunking_approaches():
    """Show the different chunking approaches using LangChain"""

    print("=== LangChain Text Splitter Comparison ===\n")

    chunker = SmartChunker()

    # Sample text for demonstration
    sample_text = """
    Natural Language Processing (NLP) is a subfield of artificial intelligence. It focuses on enabling computers to understand and process human language.

    Key NLP techniques include tokenization, part-of-speech tagging, and named entity recognition. These form the foundation for more complex tasks.

    Modern NLP relies heavily on transformer models. Models like BERT and GPT have revolutionized the field. They use attention mechanisms to understand context.

    Applications of NLP are widespread. They include machine translation, sentiment analysis, and chatbots. These tools help bridge the gap between human communication and computer understanding.

    The future of NLP looks promising. Advances in deep learning continue to improve performance. We can expect even more sophisticated language understanding capabilities.
    """

    strategies = [
        ("fixed_size", "CharacterTextSplitter"),
        ("content_aware", "RecursiveCharacterTextSplitter"),
        ("token_based", "TokenTextSplitter"),
        ("semantic", "SemanticChunker"),
    ]

    print(f"Original text: {len(sample_text)} characters\n")

    for strategy, splitter_name in strategies:
        print(f"{splitter_name} ({strategy}):")
        print("-" * 60)

        chunks = chunker.chunk_by_type(sample_text, "general", strategy)

        print(f"Number of chunks: {len(chunks)}")
        if chunks:
            avg_size = sum(len(c) for c in chunks) // len(chunks)
            print(f"Average chunk size: {avg_size} chars")

            # Show chunk boundaries
            print("Chunk boundaries:")
            for i, chunk in enumerate(chunks, 1):
                # Show first and last 40 chars of each chunk
                start = chunk[:40].replace("\n", " ").strip()
                end = (
                    chunk[-40:].replace("\n", " ").strip()
                    if len(chunk) > 40
                    else chunk.replace("\n", " ").strip()
                )
                print(f"  {i}. '{start}...' to '...{end}'")

        print()


def demonstrate_document_types():
    """Show how different document types work with LangChain splitters"""

    print("\n=== Document Type-Specific Chunking ===\n")

    chunker = SmartChunker()

    # Different document types
    documents = {
        "code": '''
def fibonacci(n):
    """Calculate nth Fibonacci number using recursion"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

class DataProcessor:
    """Process and transform data from various sources"""

    def __init__(self, data_source):
        self.data_source = data_source
        self.processed_data = []

    def process_batch(self, batch_size=100):
        """Process data in batches for memory efficiency"""
        raw_data = self.data_source.fetch_all()

        for i in range(0, len(raw_data), batch_size):
            batch = raw_data[i:i + batch_size]
            processed_batch = [self.transform_item(item) for item in batch]
            self.processed_data.extend(processed_batch)

        return self.processed_data

    def transform_item(self, item):
        """Transform individual data item"""
        # Apply business logic transformations
        return {
            'id': item.get('id'),
            'processed_at': datetime.now(),
            'value': self.normalize_value(item.get('value'))
        }
''',
        "markdown": """
# Machine Learning Pipeline

## Data Collection
The first step in any ML pipeline is collecting high-quality data. This involves:

### Data Sources
- Internal databases
- Third-party APIs
- Web scraping
- Manual annotation

### Data Quality
Ensure data meets these criteria:
- Completeness: No missing critical fields
- Accuracy: Values represent true measurements
- Consistency: Format standardization across sources

## Feature Engineering
Transform raw data into features suitable for ML models.

### Numerical Features
- Normalization and scaling
- Handling outliers
- Creating derived features

### Categorical Features
- One-hot encoding
- Label encoding
- Target encoding for high-cardinality features

## Model Training
Select and train appropriate algorithms for your use case.

### Algorithm Selection
Consider these factors:
- Problem type (classification, regression, clustering)
- Data size and dimensionality
- Interpretability requirements
- Performance constraints
""",
        "legal": """
## Terms of Service Agreement

### Section 1: Acceptance of Terms
By accessing and using this service, you accept and agree to be bound by the terms and provisions of this agreement. If you do not agree to abide by the above, please do not use this service.

### Section 2: Use License
Permission is granted to temporarily download one copy of the materials on our website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:

- modify or copy the materials
- use the materials for any commercial purpose or for any public display (commercial or non-commercial)
- attempt to decompile or reverse engineer any software contained on the website
- remove any copyright or other proprietary notations from the materials

### Section 3: Disclaimer
The materials on our website are provided on an 'as is' basis. We make no warranties, expressed or implied, and hereby disclaim and negate all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.

## Privacy Policy

### Data Collection
We collect information you provide directly to us, such as when you create an account, make a purchase, or contact us for support.

### Data Usage
We use information we collect to provide, maintain, and improve our services and develop new ones.
""",
    }

    for doc_type, content in documents.items():
        print(f"{doc_type.upper()} Document:")
        print("=" * 50)

        chunks = chunker.content_aware_chunk(content, doc_type)

        print(f"Document type: {doc_type}")
        print(f"Total chunks: {len(chunks)}")
        if chunks:
            chunk_sizes = [len(c) for c in chunks]
            print(f"Chunk sizes: {chunk_sizes} characters")
            print(f"Average size: {sum(chunk_sizes) // len(chunk_sizes)} chars")

            # Show first chunk preview
            preview = chunks[0][:150].replace("\n", " ").strip() + "..."
            print(f"First chunk preview: {preview}")

        print()


def main():
    """Run LangChain text splitter demonstrations"""
    try:
        demonstrate_chunking_approaches()
        demonstrate_document_types()

    except Exception as e:
        print(f"Demo error: {e}")
        print("Make sure all dependencies are installed: uv sync")


if __name__ == "__main__":
    main()
