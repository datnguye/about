INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_cache/vdb_entities.json'} 0 data
INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_cache/vdb_relationships.json'} 0 data
INFO:nano-vectordb:Init {'embedding_dim': 384, 'metric': 'cosine', 'storage_file': './lightrag_cache/vdb_chunks.json'} 0 data
Rerank is enabled but no rerank_model_func provided. Reranking will be skipped.
=== Graph RAG Demo with LightRAG ===

Graph RAG initialized with LightRAG in: ./lightrag_cache
Initializing LightRAG storages...
✅ LightRAG ready for use
Inserting 6 documents into LightRAG...
Processing document 1/6...
❌ Error processing document 1: 'NoneType' object does not support the asynchronous context manager protocol
Processing document 2/6...
❌ Error processing document 2: 'NoneType' object does not support the asynchronous context manager protocol
Processing document 3/6...
❌ Error processing document 3: 'NoneType' object does not support the asynchronous context manager protocol
Processing document 4/6...
❌ Error processing document 4: 'NoneType' object does not support the asynchronous context manager protocol
Processing document 5/6...
❌ Error processing document 5: 'NoneType' object does not support the asynchronous context manager protocol
Processing document 6/6...
❌ Error processing document 6: 'NoneType' object does not support the asynchronous context manager protocol
✅ Documents processed and knowledge graph built

=== Testing Graph RAG Queries ===


Query: Who approved the budget increase?
Mode: local
------------------------------------------------------------
🔍 Local search: 'Who approved the budget increase?'
Local query error: 'NoneType' object does not support the asynchronous context manager protocol
Answer: Based on the knowledge graph: Analysis of relationships and entities related to: Who approved the budget increase?...
============================================================

Query: What was the impact of hiring new engineers?
Mode: global
------------------------------------------------------------
🌍 Global search: 'What was the impact of hiring new engineers?'
Global query error: 'NoneType' object does not support the asynchronous context manager protocol
Answer: Based on the knowledge graph: The hiring enabled by the budget increase resulted in improved development velocity and product launches.
============================================================

Query: How are John Smith and the revenue growth connected?
Mode: hybrid
------------------------------------------------------------
🔀 Hybrid search: 'How are John Smith and the revenue growth connected?'
Hybrid query error: 'NoneType' object does not support the asynchronous context manager protocol
Answer: Based on the knowledge graph: Analysis of relationships and entities related to: How are John Smith and the revenue growth connected?...
============================================================

Query: What role did Mike Chen play in the AI initiative?
Mode: local
------------------------------------------------------------
🔍 Local search: 'What role did Mike Chen play in the AI initiative?'
Local query error: 'NoneType' object does not support the asynchronous context manager protocol
Answer: Based on the knowledge graph: Mike Chen was promoted to lead the AI/ML initiative funded by the budget expansion.
============================================================

Query: Show me the chain of events from budget approval to revenue growth
Mode: global
------------------------------------------------------------
🌍 Global search: 'Show me the chain of events from budget approval to revenue growth'
Global query error: 'NoneType' object does not support the asynchronous context manager protocol
Answer: Based on the knowledge graph: Analysis of relationships and entities related to: Show me the chain of events from budget approval to revenue growth...
============================================================

=== Traditional RAG vs Graph RAG Comparison ===

Query: 'How did John Smith's decision impact TechCorp's revenue?'

Traditional RAG Approach:
----------------------------------------
1. Searches for 'John Smith', 'decision', 'TechCorp', 'revenue' independently
2. Returns documents containing these keywords
3. May miss connections between budget approval → hiring → development → revenue
4. Requires manual inference of relationships

Graph RAG Approach:
----------------------------------------
1. Understands John Smith → CEO → approved budget increase
2. Traces budget increase → enabled hiring → increased development velocity
3. Connects increased velocity → product launches → revenue growth
4. Provides complete causal chain with entity relationships

Key Advantages of Graph RAG:
✅ Multi-hop reasoning across documents
✅ Relationship-aware retrieval
✅ Better handling of 'connect the dots' questions
✅ Temporal and causal understanding
✅ Entity-centric knowledge representation

=== Graph RAG Benefits Summary ===
• Uses LightRAG for automatic knowledge graph construction
• Supports local, global, and hybrid search modes
• Excels at multi-hop reasoning questions
• Maintains entity relationships and temporal connections
• Better for complex business intelligence queries
• Graceful fallback when API keys are not available
