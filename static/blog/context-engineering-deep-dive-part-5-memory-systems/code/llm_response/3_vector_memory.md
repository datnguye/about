=== Semantic Memory Demo ===
Loading embedding model: all-MiniLM-L6-v2
Storing memories...
✓ Stored: mem_0_175587... - User prefers concise code examples with comments...
✓ Stored: mem_1_175587... - Customer uses PostgreSQL 14 with Django ORM...
✓ Stored: mem_2_175587... - Debugging session: login timeout issues resolved b...
✓ Stored: mem_3_175587... - User wants cost-effective solutions, mentioned bud...
✓ Stored: mem_4_175587... - Fixed database connection pooling issue in product...
✓ Stored: mem_5_175587... - User asked about Python best practices for web dev...
✓ Stored: mem_6_175587... - Resolved memory leak in Django application by opti...
✓ Stored: mem_7_175587... - Customer prefers AWS over Google Cloud for deploym...
✓ Stored: mem_8_175587... - Implemented caching strategy using Redis for bette...
✓ Stored: mem_9_175587... - User mentioned they work with large datasets and n...

Total memories stored: 10

=== Semantic Retrieval Tests ===

Query: 'Show me efficient database code'
Relevant memories:
  1. [context] User mentioned they work with large datasets and need efficient processing
     Similarity: 0.361, Importance: 0.8, Accessed: 0 times
  2. [preference] User prefers concise code examples with comments
     Similarity: 0.342, Importance: 0.9, Accessed: 0 times

Query: 'What are the user's preferences?'
No relevant memories found above threshold

Query: 'Help with performance optimization'
Relevant memories:
  1. [solution] Implemented caching strategy using Redis for better performance
     Similarity: 0.367, Importance: 0.8, Accessed: 0 times
  2. [preference] User wants cost-effective solutions, mentioned budget constraints
     Similarity: 0.347, Importance: 0.7, Accessed: 0 times

Query: 'Cloud deployment options'
Relevant memories:
  1. [preference] Customer prefers AWS over Google Cloud for deployment
     Similarity: 0.685, Importance: 0.7, Accessed: 0 times

Query: 'Python web development advice'
Relevant memories:
  1. [query] User asked about Python best practices for web development
     Similarity: 0.837, Importance: 0.6, Accessed: 0 times

=== Memory Clustering Analysis ===

Cluster 2 (2 memories):
Sample: User prefers concise code examples with comments...
Types: {'preference': 1, 'query': 1}

Cluster 1 (6 memories):
Sample: Customer uses PostgreSQL 14 with Django ORM...
Types: {'technical_context': 1, 'solution': 4, 'context': 1}

Cluster 0 (2 memories):
Sample: User wants cost-effective solutions, mentioned budget constraints...
Types: {'preference': 2}

=== Memory Access Patterns ===
- preference: 3 memories, avg 1.0 accesses
- technical_context: 1 memories, avg 0.0 accesses
- solution: 4 memories, avg 0.2 accesses
- query: 1 memories, avg 1.0 accesses
- context: 1 memories, avg 1.0 accesses
