=== Hybrid Memory System Demo ===


--- Interaction 1 ---
Storing interaction for user user_123
✓ Stored in hot memory (Redis): I'm getting a database timeout error in my Python ...
✓ Updated warm memory (session): 1 messages
✓ Calculated importance score: 0.7999999999999999
✓ Stored in cold memory (vector): mem_1

--- Interaction 2 ---
Storing interaction for user user_123
✓ Stored in hot memory (Redis): Let's debug this step by step. First, check your c...
✓ Updated warm memory (session): 2 messages
✓ Calculated importance score: 0.7
✗ Not important enough for long-term storage

--- Interaction 3 ---
Storing interaction for user user_123
✓ Stored in hot memory (Redis): I prefer concise code examples with detailed comme...
✓ Updated warm memory (session): 3 messages
✓ Calculated importance score: 0.8999999999999999
✓ Stored in cold memory (vector): mem_2

--- Interaction 4 ---
Storing interaction for user user_123
✓ Stored in hot memory (Redis): I'll keep that in mind. Here's a concise example w...
✓ Updated warm memory (session): 4 messages
✓ Calculated importance score: 0.5
✗ Not important enough for long-term storage

--- Interaction 5 ---
Storing interaction for user user_123
✓ Stored in hot memory (Redis): What's the weather like?...
✓ Updated warm memory (session): 5 messages
✓ Calculated importance score: 0.8
✓ Stored in cold memory (vector): mem_3

==================================================

Retrieving context for user user_123, query: 'Show me how to optimize database connections'
✓ Context assembled:
  - Recent: Yes
  - Conversation: 5 messages
  - Similar past: 1 memories

=== Final Context Summary ===
Query: 'Show me how to optimize database connections'
Hot Memory: True
Warm Memory: 5 messages
Cold Memory: 1 relevant memories

Most relevant past memory:
  Content: I'm getting a database timeout error in my Python app...
  Similarity: 0.14
