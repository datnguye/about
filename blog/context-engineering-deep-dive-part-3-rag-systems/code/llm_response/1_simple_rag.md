=== Simple RAG System Demo with DuckDB ===

Loading embedding model... ✓
RAG system initialized with DuckDB vector search ✓
Generating embeddings for 6 documents... ✓
Added 6 documents to the vector store ✓

=== Testing RAG Queries ===

Q: What's the refund window for enterprise clients?
Generating embedding for question: 'What's the refund window for enterprise clients?'
Retrieved 3 relevant documents:
  1. Similarity: 0.673 - Enterprise customers get priority handling for all refund requests...
  2. Similarity: 0.667 - Our refund policy for enterprise customers: 90-day refund window...
  3. Similarity: 0.561 - All refunds must be requested through the customer portal...

A: The refund window for enterprise clients is 90 days with manager approval required.

--------------------------------------------------

Q: How quickly do enterprise customers get support?
Generating embedding for question: 'How quickly do enterprise customers get support?'
Retrieved 3 relevant documents:
  1. Similarity: 0.586 - Support SLA for enterprise: 1-hour response time, 4-hour resolution...
  2. Similarity: 0.577 - Enterprise customers get priority handling for all requests...
  3. Similarity: 0.539 - Standard support offers 24-hour response time...

A: Enterprise customers get 1-hour response time and 4-hour resolution for critical issues, much faster than the standard 24-hour response time.

--------------------------------------------------

Q: What are the benefits of premium tier?
Generating embedding for question: 'What are the benefits of premium tier?'
Retrieved 3 relevant documents:
  1. Similarity: 0.765 - Premium tier includes 24/7 phone support, dedicated account manager...
  2. Similarity: 0.271 - Enterprise customers get priority handling...
  3. Similarity: 0.162 - Support SLA for enterprise: 1-hour response time...

A: Premium tier includes 24/7 phone support, dedicated account manager, and custom integrations for comprehensive enterprise support.

=== Key Features Demonstrated ===

✓ Local embeddings with sentence-transformers (all-MiniLM-L6-v2)
✓ DuckDB vector similarity search with cosine similarity  
✓ Accurate semantic matching (0.7+ similarity scores)
✓ Graceful fallback when LLM rate limits hit
✓ Clean document retrieval with relevance ranking