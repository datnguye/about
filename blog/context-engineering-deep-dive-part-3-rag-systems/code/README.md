# RAG Systems Code Examples

This directory contains all code examples from the "RAG Systems: When Your LLM Needs to Phone a Friend" blog post.

## Table of Contents

1. [Setup](#setup)
2. [Running Examples](#running-examples)
3. [Examples Overview](#examples-overview)

## Setup

All examples use `uv` for dependency management. First, ensure you have `uv` installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the dependencies:

```bash
# Install all dependencies
uv sync
```

### API Keys Required

You'll need to set up your API keys in a `.env` file:

```bash
# Create .env file
cp .env.example .env

# Add your API keys:
# - OPENROUTER_API_KEY (for LLM calls via OpenRouter)
# - OPENAI_API_KEY (optional, for embeddings)
```

Get your free OpenRouter API key at: https://openrouter.ai/

## Running Examples

Each example can be run independently:

```bash
# Run any example
uv run 1_simple_rag.py
uv run 2_embedding_similarity.py
# ... etc
```

## Examples Overview

### 1. Simple RAG (`1_simple_rag.py`)
Basic RAG implementation showing the complete pipeline: document ingestion, embedding, retrieval, and generation.

### 2. Embedding Similarity (`2_embedding_similarity.py`)
Demonstrates how semantic similarity works with text embeddings, comparing different types of text.

### 3. Vector Database Comparison (`3_vector_db_comparison.py`)
Compares different vector databases (ChromaDB, Pinecone, Weaviate, Qdrant) for various use cases.

### 4. Smart Chunking (`4_smart_chunking.py`)
Shows different chunking strategies: fixed-size, semantic, and document-aware chunking.

### 5. Hybrid Search (`5_hybrid_search.py`)
Implements hybrid search combining BM25 keyword search with semantic similarity.

### 6. Graph RAG (`6_graph_rag.py`)
Demonstrates graph-based RAG for understanding relationships between entities.

## Dependencies

Key libraries used:
- `litellm` - Unified LLM API interface
- `chromadb` - Local vector database
- `tiktoken` - Token counting for chunking
- `numpy` - Vector operations
- `networkx` - Graph operations (for Graph RAG)
- `python-dotenv` - Environment variable management

## Notes

- All examples use free/low-cost models via OpenRouter to keep costs minimal
- ChromaDB is used for local vector storage (no external dependencies)
- Examples are designed to be educational and may need optimization for production use

## Troubleshooting

If you encounter issues:

1. Ensure all dependencies are installed: `uv sync`
2. Check your `.env` file has valid API keys
3. For ChromaDB issues, try: `rm -rf chroma_db/` to clear the local database
4. OpenRouter free tier has rate limits - wait a bit if you hit them

## Contributing

Found an issue or have an improvement? Feel free to submit a PR or open an issue!