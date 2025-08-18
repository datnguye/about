=== Hybrid Search Demo ===


Query: 'USER-12345 error logs'
----------------------------------------------------------------------
Query type detected: keyword-focused (alpha=0.3)

Top Results:

1. Score: 0.937 [██████████████████░░]
   Error logs show multiple failed login attempts from IP address 192.168.1.100.

2. Score: 0.778 [███████████████░░░░░]
   USER-12345 encountered an authentication error at 10:30 AM when trying to access the admin panel.

3. Score: 0.499 [█████████░░░░░░░░░░░]
   USER-12345 reported slow query performance on the dashboard page.

Query: 'explain the relationship between caching and performance'
----------------------------------------------------------------------
Query type detected: semantic-focused (alpha=0.8)

Top Results:

1. Score: 1.000 [████████████████████]
   The relationship between caching and database performance is complex but important.

2. Score: 0.402 [████████░░░░░░░░░░░░]
   Performance monitoring revealed bottlenecks in the authentication service.

3. Score: 0.381 [███████░░░░░░░░░░░░░]
   Database query optimization can significantly improve application performance.

Query: 'authentication security best practices'
----------------------------------------------------------------------
Query type detected: balanced (alpha=0.5)

Top Results:

1. Score: 1.000 [████████████████████]
   Understanding authentication flows is crucial for implementing secure applications.

2. Score: 0.905 [██████████████████░░]
   Performance monitoring revealed bottlenecks in the authentication service.

3. Score: 0.902 [██████████████████░░]
   Authentication tokens should be refreshed every 24 hours for security.

Query: 'SQL optimization'
----------------------------------------------------------------------
Query type detected: keyword-focused (alpha=0.3)

Top Results:

1. Score: 1.000 [████████████████████]
   Database query optimization can significantly improve application performance.

2. Score: 0.796 [███████████████░░░░░]
   SQL index strategies vary depending on query patterns and data distribution.

3. Score: 0.164 [███░░░░░░░░░░░░░░░░░]
   The relationship between caching and database performance is complex but important.


=== Search Method Comparison ===

Query: 'car maintenance problems'

Documents in collection:
1. The car manufacturer recalled vehicles due to brake issues.
2. Automobile companies must comply with safety regulations.
3. Cars need regular oil changes for optimal performance.
4. The cat jumped over the fence quickly.
5. Vehicle maintenance is essential for longevity.
6. Transportation safety standards are strictly enforced.
7. The automotive industry is shifting towards electric vehicles.
8. Cats are independent pets that require minimal care.


Keyword Only (alpha=0.0)
------------------------------------------------------------
1. [1.000] Vehicle maintenance is essential for longevity....
2. [0.833] The car manufacturer recalled vehicles due to brake issues....
3. [0.000] Automobile companies must comply with safety regulations....


Hybrid (Balanced) (alpha=0.5)
------------------------------------------------------------
1. [1.000] Vehicle maintenance is essential for longevity....
2. [0.710] The car manufacturer recalled vehicles due to brake issues....
3. [0.332] Cars need regular oil changes for optimal performance....


Semantic Only (alpha=1.0)
------------------------------------------------------------
1. [1.000] Vehicle maintenance is essential for longevity....
2. [0.665] Cars need regular oil changes for optimal performance....
3. [0.625] Automobile companies must comply with safety regulations....


=== Reranking for Diversity (MMR) ===

Query: 'Python programming'

Standard Ranking (may have redundancy):
------------------------------------------------------------
1. [1.000] Python is a high-level programming language.
2. [0.924] Python programming is popular for data science.
3. [0.534] Python's syntax is clear and readable.
4. [0.488] Java is an object-oriented programming language.
5. [0.468] Machine learning models can be built with Python.

MMR Reranking (promotes diversity):
------------------------------------------------------------
1. Python is a high-level programming language.
2. Python programming is popular for data science.
3. Java is an object-oriented programming language.
4. Python's syntax is clear and readable.
5. Machine learning models can be built with Python.
