+++
title = "RAG Systems: When Your LLM Needs to Phone a Friend (Your Database)"
description = "LLMs know a lot, but they don't know YOUR data. RAG changes that — and if you're not using it yet, you're leaving value on the table. Let's build knowledge-aware AI systems."
date = 2025-08-18
template = "blog_page.html"

[extra]
authors = [
  { name = "Dat Nguyen", title = "Data & AI @ Tech Lead", github = "datnguye", linkedin = "datnguye" }
]
tags = ["RAG", "VectorDatabase", "Embeddings", "Retrieval", "Pinecone", "ChromaDB", "LLM", "ContextEngineering"]
read_time = "10 min read"
featured_image = "/blog/context-engineering-deep-dive-part-3-rag-systems/hero.png"
toc = true
toc_depth = 1
show_ads = true
enable_auto_related = true
+++

![Visualization of RAG architecture showing document chunks flowing through embeddings into a vector database, with retrieval connecting to an LLM for augmented generation](/blog/context-engineering-deep-dive-part-3-rag-systems/hero.png)

First, let's get something straight. LLMs know a lot, but they don't know YOUR data. They can't access your company's documentation, your product specs, or that critical decision from last Tuesday's meeting. RAG changes that — and if you're not using it yet, you're leaving value on the table.

## Knowledge Problem

Here's a fun experiment. Ask ChatGPT about your company's API rate limits. Watch it confidently make up numbers. Now ask it about your product's pricing tiers from last month. More creative fiction. That's not a bug — it's the fundamental limitation we're solving.

The problem isn't that LLMs are dumb. They just don't have access to YOUR specific information. It's like having a brilliant consultant who's never seen your company's documents.

Even the best [prompting techniques](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/) and [reasoning agents](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/) can't help if the LLM simply doesn't have access to the information it needs. That's where RAG comes in.

### Use Traditional Search?

You've probably tried this:

```python
# The naive approach that fails spectacularly
user_question = "What's our refund policy for enterprise customers?"
search_results = database.search(user_question)  # Returns 500 documents
llm_prompt = f"Answer this: {user_question}\nContext: {search_results[:10]}"
# LLM: "Based on document 3, paragraph 2... *proceeds to hallucinate*"
```

Keyword search gives you documents with the word "refund" and "enterprise". But your actual policy might be in a document titled "Service Level Agreements" that never mentions those exact words. Classic search fail.

### Use Fine-Tuning?

Before you ask: "Can't I just fine-tune the model on my data?"

Let me save you 💰💰💰 and 🕥🕥🕥 of frustration:

- [Fine-tuning](https://huggingface.co/blog/dvgodoy/fine-tuning-llm-hugging-face) teaches behavior, not facts
- Your data changes daily (fine-tuning doesn't)
- It's expensive and slow to update
- The model will still hallucinate specific details

Fine-tuning is for teaching style and patterns. RAG is for injecting knowledge. Pick your battle wisely.

## 1. RAG Fundamentals

[RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) isn't just "search + LLM". It's a coordinated process that combines smart retrieval with intelligent generation. Here's how it works:

### RAG Pipeline in Action

Here's what happens when you ask a RAG system a question:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  User Question  │───▶│  Embed Question  │───▶│ Vector Database │
│  "What's our    │    │     (Vector)     │    │     Search      │
│   policy?"      │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Final Answer   │◀───│   LLM Generate   │◀───│ Retrieve Docs   │
│ "Based on our   │    │   with Context   │    │  (Top matches)  │
│  policy..."     │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

The key components are:
- **Embedding Strategy** — Convert text to vectors that capture semantic meaning
- **Vector Store Database** — Store and efficiently search millions of embeddings
- **Similarity Search** — Find the most relevant documents using [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

And if we look at the code, here is the simple demonstration:

```python
class SimpleRAG:
    def query(self, question: str) -> str:
        # Step 1: Embed the question
        query_embedding = embedding(model="text-embedding-3-small", input=question)
        
        # Step 2: Retrieve relevant documents
        results = self.collection.query(query_embeddings=[query_embedding])
        
        # Step 3: Build context from retrieved documents
        context = "\n\n".join(results['documents'][0])
        
        # Step 4: Generate answer using LLM with context
        response = completion(
            model="openrouter/openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer based on context."},
                {"role": "user", "content": f"Context: {context}\nQ: {question}"}
            ]
        )
        return response.choices[0].message.content

# Usage
rag = SimpleRAG()
rag.add_documents(["Enterprise refund policy: 90 days with approval"])
answer = rag.query("What's the refund window for enterprise?")
```

{{ code_example(
  script="1_simple_rag.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/1_simple_rag.py",
  command="uv run 1_simple_rag.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/1_simple_rag.md"
) }}

### Retrieval-Generation Balance

Too much context? The LLM gets confused. Too little? It starts making things up. Here's how to get it right:

```python
def smart_retrieval(question: str, documents: List[str]) -> str:
    # Retrieve more than you need
    initial_results = retrieve_documents(question, n=10)
    
    # Re-rank by relevance
    reranked = rerank_by_relevance(initial_results, question)
    
    # Take only highly relevant documents (threshold filtering)
    relevant_docs = [doc for doc in reranked if doc.score > 0.7]
    
    return generate_answer(question, relevant_docs[:3])  # Top 3
```

The good is in the balance. Cast a wide net, filter smartly, then serve only the best knowledge to your LLM.

## 2. The Embedding Game

Embeddings are where text becomes math which let computers understand that "car" and "automobile" mean the same thing, while "car" and "carpet" don't — even though they share three letters.

### Text to Vectors

Think of embeddings as GPS coordinates for meaning. Just like latitude and longitude tell you where something is physically, embedding vectors tell you where text sits in "meaning space".

```python
def semantic_similarity(text1: str, text2: str) -> float:
    # Convert texts to vectors
    embed1 = embedding(model="text-embedding-3-small", input=text1)
    embed2 = embedding(model="text-embedding-3-small", input=text2)
    
    # Calculate cosine similarity
    return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

# Test semantic understanding
examples = [
    ("cat sat on mat", "feline rested on rug"),     # 0.842 - Same meaning
    ("SELECT * FROM users", "Get all user records"), # 0.756 - Technical similarity
    ("bug", "defect"),                               # 0.834 - Synonyms
    ("bug", "insect"),                               # 0.672 - Different context
]
```

{{ code_example(
  script="2_embedding_similarity.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/2_embedding_similarity.py",
  command="uv run 2_embedding_similarity.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/2_embedding_similarity.md"
) }}

### Choosing the Right Embedding Model

Not all embedding models are created equal. With dozens available, picking the wrong one wastes weeks. Here are the ones that actually matter:

| Model | Dimensions | Best For | Speed | Quality |
|-------|------------|----------|-------|---------|
| **all-MiniLM-L6-v2** | 384 | General purpose, fast prototypes | ⚡⚡⚡ | ⭐⭐⭐ |
| **text-embedding-3-small** | 1536 | Production apps, balanced cost/quality | ⚡⚡ | ⭐⭐⭐⭐ |
| **text-embedding-3-large** | 3072 | High-accuracy search, enterprise | ⚡ | ⭐⭐⭐⭐⭐ |

**Rule of thumb**: Start with `all-MiniLM-L6-v2` for prototypes, upgrade to `text-embedding-3-small` for production.

{% tip(type="note", title="Share Your Experience") %}
Found a better embedding model for your use case? Drop your recommendations in the comments below — the community learns from real battle-tested experiences!
{% end %}

## 3. Vector Database

Your vector database choice depends on where you want to run it and how much control you need.

For **local development** and prototypes where you want full control, your best bets are [ChromaDB](https://docs.trychroma.com/docs/embeddings/embedding-functions) (free, dead simple setup, handles 1M+ vectors locally) or [DuckDB + VSS](https://duckdb.org/2024/05/03/vector-similarity-search-vss.html) (free, SQL-native, great for analytics teams who love SQL).

When you're ready for **production scale** with zero ops overhead, consider managed cloud services like [Pinecone](https://www.pinecone.io/) or [Snowflake](https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings).

For the demo purpose in this article, let's quacking use DuckDB with vector similarity search (VSS) extension offers a compelling middle ground:

```python
import duckdb
from sentence_transformers import SentenceTransformer

# Initialize DuckDB with VSS extension
conn = duckdb.connect(":memory:")
conn.execute("INSTALL vss")
conn.execute("LOAD vss")

# Create vector table
conn.execute("""
    CREATE TABLE documents (
        id INTEGER PRIMARY KEY,
        content TEXT,
        embedding FLOAT[384]
    )
""")

# Add documents with embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
docs = ["Python is great for data science", "SQL handles structured data well"]

for i, doc in enumerate(docs):
    embedding = model.encode([doc])[0].tolist()
    conn.execute("""
        INSERT INTO documents (id, content, embedding) 
        VALUES (?, ?, ?)
    """, [i, doc, embedding])

# Semantic search using SQL
query_embedding = model.encode(["data analysis"]).tolist()[0]
results = conn.execute("""
    SELECT content, array_cosine_similarity(embedding, ?) as similarity
    FROM documents
    ORDER BY similarity DESC
    LIMIT 3
""", [query_embedding]).fetchall()
```

Perfect for teams that live in SQL and want vector search without leaving their comfort zone.

Let's circle back to the [RAG pipeline](#1-rag-fundamentals) code example and break it safely if you'd like to give a try to another type of vector database.

## 4. Chunking Strategy

Here's a dirty secret: 90% of RAG failures happen at the chunking stage. You can have the best embeddings and the fanciest vector database, but if your chunks (or text splitter) are garbage, your RAG is garbage.

There are three main approaches to text chunking, each with their own trade-offs:

**1. Fixed-size chunking** — Split by character count or token count. Simple but dumb. Breaks sentences mid-word.

**2. Content-aware chunking** — Split by document structure (paragraphs, sections, sentences). Preserves meaning but variable sizes.

**3. Semantic chunking** — Split by meaning similarity. Groups related sentences together. Most intelligent but computationally expensive.

That's what the tutorials say. But here's what they don't tell you:

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter, 
    CodeTextSplitter,
    SemanticChunker
)
from sentence_transformers import SentenceTransformer

class SmartChunker:
    def __init__(self):
        # Content-aware splitter (most common)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]  # Try these in order
        )
        
        # Code-aware splitter
        self.code_splitter = CodeTextSplitter.from_language(
            language="python",
            chunk_size=1500,
            chunk_overlap=200
        )
        
        # Semantic splitter (experimental)
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.semantic_splitter = SemanticChunker(embedding_model)
    
    def chunk_by_type(self, text: str, doc_type: str) -> list[str]:
        """Choose chunking strategy based on document type"""
        
        if doc_type == 'code':
            # Respect function/class boundaries
            return self.code_splitter.split_text(text)
            
        elif doc_type == 'legal':
            # Keep legal sections together
            legal_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=300,
                separators=["\n\n## ", "\n\n### ", "\n\n", "\n"]
            )
            return legal_splitter.split_text(text)
            
        elif doc_type == 'semantic':
            # Group by meaning (slower but better quality)
            return self.semantic_splitter.split_text(text)
            
        else:
            # Default content-aware chunking
            return self.text_splitter.split_text(text)

# Different strategies for different content
chunker = SmartChunker()
code_chunks = chunker.chunk_by_type(python_code, 'code')
legal_chunks = chunker.chunk_by_type(contract_text, 'legal') 
semantic_chunks = chunker.chunk_by_type(research_paper, 'semantic')
```

{{ code_example(
  script="4_smart_chunking.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/4_smart_chunking.py",
  command="uv run 4_smart_chunking.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/4_smart_chunking.md"
) }}

## 5. Retrieval Optimization

Retrieval is where good RAG systems become great. It's not about finding documents — it's about finding the RIGHT documents in the RIGHT order. And the optimization comes with _Hybrid Search_, _Re-ranking_ and _Metadata Filtering_. Let's break down.

### Hybrid Search

Why choose between keyword and semantic search when you can have both?

```python
class HybridSearcher:
    def __init__(self, alpha: float = 0.5):  # 0=keyword, 1=semantic
        self.alpha = alpha
    
    def hybrid_search(self, query: str, documents: List[str]) -> List[Tuple[str, float]]:
        # Get BM25 (keyword) and semantic scores
        keyword_scores = self._bm25_search(query, documents)
        semantic_scores = self._semantic_search(query, documents)
        
        # Normalize and combine scores
        combined_scores = {}
        for doc in documents:
            kw_score = self._normalize(keyword_scores.get(doc, 0))
            sem_score = self._normalize(semantic_scores.get(doc, 0))
            combined_scores[doc] = (1 - self.alpha) * kw_score + self.alpha * sem_score
        
        return sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    
    def adaptive_search(self, query: str, documents: List[str]):
        # Auto-adjust based on query type
        if self._is_specific_term(query):  # IDs, codes
            self.alpha = 0.3  # Favor keyword
        elif self._is_conceptual(query):   # "explain", "how", "why"
            self.alpha = 0.8  # Favor semantic
        else:
            self.alpha = 0.5  # Balanced
        
        return self.hybrid_search(query, documents)
```

{{ code_example(
  script="5_hybrid_search.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/5_hybrid_search.py",
  command="uv run 5_hybrid_search.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/5_hybrid_search.md"
) }}

### Re-ranking Strategy

First retrieval is never perfect. Re-ranking fixes that.

We'll see below code samples with [Cross Encoder Rerank](https://sbert.net/examples/cross_encoder/applications/README.html):

```python
from sentence_transformers import se

class ReRanker:
    def cross_encoder_rerank(self, query: str, documents: List[str], top_k: int = 3):
        """Use cross-encoder for precise re-ranking"""
        model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        pairs = [[query, doc] for doc in documents]
        scores = model.predict(pairs)
        doc_scores = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
        
        return [doc for doc, _ in doc_scores[:top_k]]
```

### Metadata Filtering

Why must we always similarity-search on the whole thing, but on just a subset with some filtering done in prior. That's the key!

```python
class MetadataEnhancedRAG:
    def add_document_with_metadata(self, text: str, metadata: Dict):
        # Auto-enrich metadata
        enriched_metadata = {
            **metadata,
            'char_count': len(text),
            'has_code': '```' in text or 'def ' in text,
            'complexity': self._estimate_complexity(text),
            'date_added': datetime.now().isoformat()
        }
        
        self.collection.add(documents=[text], metadatas=[enriched_metadata])
    
    def smart_query(self, query: str, user_context: Dict = None):
        # Auto-detect filters from query
        filters = {}
        if 'recent' in query.lower():
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            filters['date_added'] = {'$gte': week_ago}
        
        if 'code' in query.lower():
            filters['has_code'] = True
        
        # Apply user context
        if user_context and user_context.get('technical_level') == 'beginner':
            filters['complexity'] = {'$lte': 3}
        
        return self.collection.query(query_texts=[query], where=filters)
```

## 6. Graph-based RAG

Here's where RAG gets interesting. Traditional RAG treats documents as isolated chunks (the island!). Graph RAG understands relationships — and that changes everything.

Imagine asking "Who approved the budget increase that led to the Q3 hiring?" Traditional RAG searches for "budget", "increase", "Q3", "hiring" separately. Graph RAG follows the connections: budget document → approval record → personnel changes.

```python
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from sentence_transformers import SentenceTransformer
from litellm import acompletion

class GraphRAGDemo:
    def __init__(self, working_dir: str = "./lightrag_cache"):
        # Initialize local embedding model
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Custom embedding function
        async def embedding_func(texts):
            if isinstance(texts, str):
                texts = [texts]
            embeddings = self.embedding_model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        
        # Custom LLM function using OpenRouter
        async def llm_func(prompt, system_prompt=None, **kwargs):
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await acompletion(
                model="openrouter/openai/gpt-oss-20b:free",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                messages=messages
            )
            return response.choices[0].message.content
        
        # Initialize LightRAG
        self.rag = LightRAG(
            working_dir=working_dir,
            embedding_func=EmbeddingFunc(embedding_dim=384, func=embedding_func),
            llm_model_func=llm_func,
            chunk_token_size=1200,
            top_k=10,
            max_entity_tokens=5000
        )
    
    async def insert_documents(self, documents: list[str]):
        # LightRAG automatically builds knowledge graph from documents
        for doc in documents:
            await self.rag.ainsert(doc.strip())
    
    async def query_local(self, query: str) -> str:
        # Local mode: focus on specific entities and direct relationships
        return await self.rag.aquery(query, param=QueryParam(mode="local"))
    
    async def query_global(self, query: str) -> str:
        # Global mode: broader context across entire knowledge graph
        return await self.rag.aquery(query, param=QueryParam(mode="global"))
    
    async def query_hybrid(self, query: str) -> str:
        # Hybrid mode: combines local and global approaches
        return await self.rag.aquery(query, param=QueryParam(mode="hybrid"))

# Usage
graph_rag = GraphRAGDemo()
await graph_rag.insert_documents(business_docs)
answer = await graph_rag.query_hybrid("How did the budget approval lead to revenue growth?")
```

{{ code_example(
  script="6_graph_rag.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/6_graph_rag.py",
  command="uv run 6_graph_rag.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/6_graph_rag.md"
) }}

Graph RAG shines when your data has rich relationships (org charts, knowledge bases, research papers), questions involve multiple hops ("Who worked on the project that influenced X?"), you need to trace causality or dependencies, and context comes from connections rather than just content. But skip it when you have simple Q&A needs, documents are independent, you need real-time responses (graph traversal adds latency), or your team lacks graph database experience.

## Key Takeaways

- **RAG > Fine-tuning for facts** — Fine-tuning teaches behavior, RAG injects knowledge. Use RAG for dynamic, factual information
- **Hybrid search wins** — Combine keyword (BM25) and semantic search. Let keywords find specifics, semantics find concepts
- **Graph RAG for relationships** — When your questions involve "who", "how", and "why" across multiple documents, graphs beat flat vectors

## What's Next?

Great, your agents can think and access knowledge. But how do they actually DO things? Time to talk about action tools...

---

*Technical deep dive series — Part 3 of 5*

**[← Part 2: Agents & Reasoning](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)** | **[Part 4: Action Tools →](/blog/internal/context-engineering-deep-dive-part-4-action-tools/)**

## Related Articles in This Series

📚 **Context Engineering Deep Dive Series:**

1. [User Intent & Prompting: The Art of Making LLMs Understand What You Really Want](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)
2. [Agents & Reasoning: When LLMs Learn to Think Before They Speak](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)
3. **RAG Systems** (You are here)
4. [Action Tools: How LLMs Finally Learned to Stop Talking and Start Doing](/blog/internal/upcoming/)
5. [Memory Systems: Teaching LLMs to Remember (Without Going Broke)](/blog/internal/upcoming/)

🎯 **Start with the overview:** [Context Engineering: How RAG, agents, and memory make LLMs actually useful](/blog/internal/context-engineering-modern-llm-ecosystem/)