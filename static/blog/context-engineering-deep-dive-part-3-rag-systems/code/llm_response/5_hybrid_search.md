======================================================================
HYBRID SEARCH DEMONSTRATION
======================================================================

Documents in collection:
1. USER-12345 encountered authentication error at 10:30 AM
2. The authentication system uses OAuth 2.0 for secure verification
3. Error code AUTH-500 indicates server-side authentication failure
4. Understanding how authentication works is crucial for security
5. Database query optimization improves application performance
6. ORDER-67890 was processed successfully at 11:45 AM
7. Explain the relationship between caching and database performance
8. API-KEY-789 expired and needs renewal

======================================================================
SEARCH RESULTS
======================================================================

🔍 Query: 'USER-12345 error'
--------------------------------------------------
  → Detected specific terms, using alpha=0.3 (keyword-focused)

Top 3 Results:

  1. [████████████████████] Score: 1.000
     USER-12345 encountered authentication error at 10:30 AM

  2. [███████░░░░░░░░░░░░░] Score: 0.398
     Error code AUTH-500 indicates server-side authentication failure

  3. [██░░░░░░░░░░░░░░░░░░] Score: 0.111
     ORDER-67890 was processed successfully at 11:45 AM

🔍 Query: 'explain authentication security'
--------------------------------------------------
  → Detected conceptual query, using alpha=0.8 (semantic-focused)

Top 3 Results:

  1. [████████████████████] Score: 1.000
     Understanding how authentication works is crucial for security

  2. [█████████░░░░░░░░░░░] Score: 0.479
     The authentication system uses OAuth 2.0 for secure verification

  3. [███████░░░░░░░░░░░░░] Score: 0.385
     Explain the relationship between caching and database performance

🔍 Query: 'authentication OAuth'
--------------------------------------------------
  → Using balanced search, alpha=0.5

Top 3 Results:

  1. [████████████████████] Score: 1.000
     The authentication system uses OAuth 2.0 for secure verification

  2. [███████░░░░░░░░░░░░░] Score: 0.399
     Understanding how authentication works is crucial for security

  3. [█████░░░░░░░░░░░░░░░] Score: 0.295
     Error code AUTH-500 indicates server-side authentication failure

🔍 Query: 'ORDER-67890'
--------------------------------------------------
  → Detected specific terms, using alpha=0.3 (keyword-focused)

Top 3 Results:

  1. [████████████████████] Score: 1.000
     ORDER-67890 was processed successfully at 11:45 AM

  2. [██░░░░░░░░░░░░░░░░░░] Score: 0.131
     API-KEY-789 expired and needs renewal

  3. [█░░░░░░░░░░░░░░░░░░░] Score: 0.088
     USER-12345 encountered authentication error at 10:30 AM

🔍 Query: 'how does caching work'
--------------------------------------------------
  → Detected conceptual query, using alpha=0.8 (semantic-focused)

Top 3 Results:

  1. [████████████████████] Score: 1.000
     Explain the relationship between caching and database performance

  2. [█████████░░░░░░░░░░░] Score: 0.496
     Understanding how authentication works is crucial for security

  3. [██████░░░░░░░░░░░░░░] Score: 0.319
     Database query optimization improves application performance

======================================================================
MANUAL ALPHA CONTROL COMPARISON
======================================================================

🔍 Query: 'authentication system security'

Keyword-only (alpha=0.0):
------------------------------
  1. [1.000] Understanding how authentication works is crucial for securi...
  2. [0.944] The authentication system uses OAuth 2.0 for secure verifica...

Balanced (alpha=0.5):
------------------------------
  1. [1.000] Understanding how authentication works is crucial for securi...
  2. [0.843] The authentication system uses OAuth 2.0 for secure verifica...

Semantic-only (alpha=1.0):
------------------------------
  1. [1.000] Understanding how authentication works is crucial for securi...
  2. [0.742] The authentication system uses OAuth 2.0 for secure verifica...
