"""
Demonstrate Graph RAG using LightRAG with DeepSeek for LLM and embeddings
Based on: https://github.com/HKUDS/LightRAG/blob/main/examples/lightrag_openai_compatible_demo.py
"""

import asyncio
import os
import shutil
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.llm.openai import openai_complete_if_cache
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer

load_dotenv()


async def llm_model_func(
    prompt: str,
    system_prompt: str | None = None,
    history_messages: list | None = None,
    **kwargs,
) -> str:
    """
    Custom LLM function using DeepSeek API
    """
    return await openai_complete_if_cache(
        "deepseek-chat",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages or [],
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        **kwargs,
    )


# Initialize local embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


async def local_embedding_func(texts: list[str]) -> np.ndarray:
    """
    Local embedding function using SentenceTransformer
    """
    if isinstance(texts, str):
        texts = [texts]

    # Generate embeddings locally
    embeddings = embedding_model.encode(texts, convert_to_numpy=True)
    return embeddings


class GraphRAGDemo:
    """Demonstrate Graph RAG with relationship understanding using LightRAG"""

    def __init__(self, working_dir: str = "./lightrag_demo"):
        """Initialize LightRAG with DeepSeek for LLM and local embeddings"""

        self.working_dir = working_dir

        # Clean working directory to avoid state issues
        if Path(working_dir).exists():
            shutil.rmtree(working_dir)

        # Configure LightRAG with DeepSeek for LLM and local embeddings
        self.rag = LightRAG(
            working_dir=working_dir,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=384,  # all-MiniLM-L6-v2 dimension
                max_token_size=8192,
                func=local_embedding_func,
            ),
        )

        print(f"✓ LightRAG initialized at {working_dir}")

    async def add_documents(self, documents: list[str]):
        """Add documents and build knowledge graph using LightRAG"""
        print(f"Building knowledge graph from {len(documents)} documents...")

        for _i, doc in enumerate(documents, 1):
            await self.rag.ainsert(input=doc.strip())

        print("✓ Knowledge graph built")

    async def query_local(self, question: str) -> str:
        """
        Local query mode: Focus on specific entities and direct relationships
        """
        try:
            response = await self.rag.aquery(question, param=QueryParam(mode="local"))
            return response
        except Exception as e:
            return f"Local query error: {str(e)[:200]}..."

    async def query_global(self, question: str) -> str:
        """
        Global query mode: Broader context across entire knowledge graph
        """
        try:
            response = await self.rag.aquery(question, param=QueryParam(mode="global"))
            return response
        except Exception as e:
            return f"Global query error: {str(e)[:200]}..."

    async def query_hybrid(self, question: str) -> str:
        """
        Hybrid query mode: Combines local and global approaches
        """
        try:
            response = await self.rag.aquery(question, param=QueryParam(mode="hybrid"))
            return response
        except Exception as e:
            return f"Hybrid query error: {str(e)[:200]}..."


async def demonstrate_lightrag():
    """Demonstrate LightRAG Graph RAG capabilities"""

    print("LIGHTRAG GRAPH RAG DEMONSTRATION")
    print("Using DeepSeek API for LLM and Local Embeddings")

    # Sample documents with rich entity relationships
    documents = [
        """
        Sarah Chen is the CEO of TechCorp, a technology company founded in 2020.
        She previously worked as Chief Technology Officer at DataSystems for 5 years.
        Under her leadership, TechCorp successfully secured $50 million in Series B
        funding led by VentureCapital Partners in Q3 2023. This funding round was
        critical for the company's growth strategy.
        """,
        """
        The Series B funding round enabled TechCorp to significantly expand their
        engineering capabilities. Mike Johnson, who was recruited by Sarah Chen
        from CloudNet in 2021, now leads the engineering department as VP of Engineering.
        The team has grown from 15 to 45 engineers under his leadership.
        """,
        """
        TechCorp's flagship product, SmartAnalytics, was developed under Mike Johnson's
        engineering leadership. The core machine learning algorithms were designed by
        Lisa Wang, who serves as Lead ML Engineer on the SmartAnalytics team.
        The platform processes over 1 billion data points daily for Fortune 500 clients.
        """,
        """
        Lisa Wang's algorithmic innovations in SmartAnalytics have directly contributed
        to TechCorp's impressive revenue growth trajectory. The company's revenue
        increased from $5 million in 2021 to $25 million in 2023, a 400% growth.
        Her algorithms reduced data processing time by 80% for major clients.
        """,
        """
        The $50 million Series B funding secured by Sarah Chen will be strategically
        invested to expand SmartAnalytics into European markets. Additionally,
        Lisa Wang's team will lead the development of SmartAnalytics 2.0 with
        advanced predictive analytics features. This expansion is projected to
        double the company's revenue by 2025.
        """,
    ]

    # Initialize LightRAG Graph RAG
    graph_rag = GraphRAGDemo()
    await graph_rag.rag.initialize_storages()
    await initialize_pipeline_status()

    # Build knowledge graph
    await graph_rag.add_documents(documents)

    # Test relationship-focused queries
    print("\nTesting Graph RAG Query Modes:")

    relationship_queries = [
        ("Who developed the core algorithms for SmartAnalytics?", "local"),
        ("How did the Series B funding impact TechCorp's growth strategy?", "global"),
        (
            "What's the connection between Sarah Chen and the company's revenue growth?",
            "hybrid",
        ),
    ]

    for question, mode in relationship_queries:
        print(f"\nQuery ({mode}): '{question}'")

        if mode == "local":
            answer = await graph_rag.query_local(question)
        elif mode == "global":
            answer = await graph_rag.query_global(question)
        else:
            answer = await graph_rag.query_hybrid(question)

        print(f"Answer: {answer}")

    # Compare different query modes on the same question
    print("\nComparing Query Modes:")

    comparison_query = (
        "How did Sarah Chen's leadership decisions impact TechCorp's success?"
    )
    print(f"\nQuestion: '{comparison_query}'")

    modes = [("Local", "local"), ("Global", "global"), ("Hybrid", "hybrid")]

    for mode_name, mode in modes:
        if mode == "local":
            answer = await graph_rag.query_local(comparison_query)
        elif mode == "global":
            answer = await graph_rag.query_global(comparison_query)
        else:
            answer = await graph_rag.query_hybrid(comparison_query)

        display_answer = answer[:300] + "..." if len(answer) > 300 else answer
        print(f"\n{mode_name}: {display_answer}")

    # Demo completed


async def main():
    """Run the LightRAG Graph RAG demonstration"""
    try:
        await demonstrate_lightrag()
    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
