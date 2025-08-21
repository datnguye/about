+++
title = "RAG Systems: When Your LLM Needs to Phone a Friend (Your Database)"
description = "LLMs know a lot, but they don't know YOUR data. RAG changes that — and if you're not using it yet, you're leaving value on the table. Let's build knowledge-aware AI systems."
date = 2025-08-19
template = "blog_page.html"

[extra]
authors = [
  { name = "Dat Nguyen", title = "Data & AI @ Tech Lead", github = "datnguye", linkedin = "datnguye" }
]
tags = ["RAG", "VectorDatabase", "Embeddings", "HybridSearch", "BM25", "GraphRAG", "LightRAG", "ContextEngineering"]
read_time = "7 min read"
featured_image = "/blog/context-engineering-deep-dive-part-3-rag-systems/hero.png"
toc = true
toc_depth = 1
show_ads = true
enable_auto_related = true
+++

![Visualization of RAG architecture showing document chunks flowing through embeddings into a vector database, with retrieval connecting to an LLM for augmented generation](/blog/context-engineering-deep-dive-part-3-rag-systems/hero.png)

LLMs don't know YOUR data. They can't access your company docs, product specs, or that critical decision from last Tuesday. That's not a bug — it's a feature (😆) so that why RAG exists.

## The Knowledge Gap

Ask ChatGPT about your API rate limits? Creative fiction. Your pricing tiers? More fiction. Even the best [prompting](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/) and [agents](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/) can't help if the knowledge isn't there.

**Traditional search?** Returns 500 documents with the word "refund". Your actual policy is in "Service Level Agreements" — no match.

**Fine-tuning?** Teaches behavior, not facts. Your data changes daily. It's expensive. Save your 💰💰💰.

So how do we bridge this knowledge gap? Enter RAG — the pattern that actually works.

## 1. RAG Fundamentals

[RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation), Retrieval-Augmented Generation, isn't just "search + LLM". It's a coordinated process that combines smart retrieval with intelligent generation. Here's how it works:

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

And if we look at the code, here is the simple illustration:

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

But here's the thing — none of this works without turning your text into numbers first.

## 2. Embeddings: Text Becomes Math

Think of embeddings as GPS coordinates for meaning. Just like latitude and longitude tell you where something is physically, embedding vectors tell you where text sits in "meaning space". This lets computers understand that "car" and "automobile" mean the same thing.

### Choosing the Right Model

Not all embedding models are created equal. With dozens available, picking the wrong one wastes weeks. Here are the ones that actually matter (in my limited experiences):

| Model | Dimensions | Best For | Speed | Quality |
|-------|------------|----------|-------|---------|
| **all-MiniLM-L6-v2** | 384 | General purpose, fast prototypes | ⚡⚡⚡ | ⭐⭐⭐ |
| **text-embedding-3-small** | 1536 | Production apps, balanced cost/quality | ⚡⚡ | ⭐⭐⭐⭐ |
| **text-embedding-3-large** | 3072 | High-accuracy search, enterprise | ⚡ | ⭐⭐⭐⭐⭐ |

**Rule of thumb**: Start with `all-MiniLM-L6-v2` for prototypes, upgrade to `text-embedding-3-small` for production.

Once you've got your embeddings, you need somewhere to store them — and that's where vector databases come in.

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

Now, even with perfect embeddings and a blazing-fast vector database, there's one thing that kills most RAG systems before they even start.

## 4. Chunking: Where 90% of RAG Fails

Three approaches, pick wisely:

1. **Fixed-size** — Split by 1000 chars. Simple but breaks sentences
2. **Content-aware** — Split by paragraphs/sections. Preserves meaning
3. **Semantic** — Group by meaning. Smart but slow

**Pro tip:** Match chunking to content type:
- Code → Respect function boundaries (1500 chars)
- Legal → Keep sections intact (2000 chars)  
- General → Recursive split with 200 char overlap

{{ code_example(
  script="4_smart_chunking.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/4_smart_chunking.py",
  command="uv run 4_smart_chunking.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/4_smart_chunking.md"
) }}

You've chunked your documents perfectly. Now let's make sure you're actually finding the right ones.

## 5. Retrieval Optimization

2 techniques that actually matter:

### Hybrid Search: Best of Both Worlds

Combine keyword (BM25) and semantic search. Let keywords find specifics ("ORDER-12345"), semantics find concepts ("refund process").

```python
def hybrid_search(query: str, alpha: float = 0.5):  # 0=keyword, 1=semantic
    # Auto-adjust based on query type
    if has_specific_terms(query):  # IDs, codes
        alpha = 0.3  # Favor keyword
    elif is_conceptual(query):     # "explain", "how"
        alpha = 0.8  # Favor semantic
    
    keyword_scores = bm25_search(query)
    semantic_scores = vector_search(query)
    return combine_scores(keyword_scores, semantic_scores, alpha)
```

{{ code_example(
  script="5_hybrid_search.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/5_hybrid_search.py",
  command="uv run 5_hybrid_search.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/5_hybrid_search.md"
) }}

### Re-ranking & Metadata

**Re-ranking**: First retrieval gets 10 docs, cross-encoder picks the best 3. More accurate than single-pass.

**Metadata filtering**: Don't search everything. Filter by date, type, or complexity BEFORE similarity search.

That covers traditional RAG. But what if your data isn't just documents — what if it's a web of connections?

## 6. Graph RAG

Traditional RAG treats documents as isolated chunks. Graph RAG understands relationships.

**Example**: "Who approved the budget increase that led to Q3 hiring?"
- Traditional RAG: Searches "budget", "increase", "Q3", "hiring" separately
- Graph RAG: Follows connections: budget → approval → personnel changes

Graph RAG works best for rich relationships (org charts, research papers), multi-hop questions ("Who worked on X that influenced Y?"), and causality tracing, but skip it for simple Q&A, real-time needs (graphs add latency), or teams lacking graph database experience.

Graph RAG essentially steps through: **1) Entity extraction** — Pull people, companies, events from documents, **2) Relationship mapping** — Connect how Sarah → hired Mike → built SmartAnalytics, **3) Graph storage** — Store as nodes (entities) and edges (relationships), **4) Graph traversal or query** — Follow connections to answer multi-hop questions like "Who's responsible for the revenue impact of the Series B funding?".

Building graph databases used to be complex, but frameworks like [LightRAG](https://github.com/HKUDS/LightRAG) now handle the heavy lifting automatically.

{{ code_example(
  script="6_graph_rag.py",
  script_url="/blog/context-engineering-deep-dive-part-3-rag-systems/code/6_graph_rag.py",
  command="uv run 6_graph_rag.py",
  output="/blog/context-engineering-deep-dive-part-3-rag-systems/code/llm_response/6_graph_rag.md"
) }}

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
4. [Action Tools: How LLMs Finally Learned to Stop Talking and Start Doing](/blog/internal/context-engineering-deep-dive-part-4-action-tools/)
5. [Memory Systems: Teaching LLMs to Remember (Without Going Broke)](/blog/internal/upcoming/)

🎯 **Start with the overview:** [Context Engineering: How RAG, agents, and memory make LLMs actually useful](/blog/internal/context-engineering-modern-llm-ecosystem/)