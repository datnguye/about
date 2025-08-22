=== Entity Memory Demo ===

Processing conversation messages...
1. The user mentioned their app has database performance issues
   Found entities: ['person_user', 'project_app', 'technology_database', 'concept_issue']

2. The customer is using PostgreSQL with their Django app
   Found entities: ['person_customer', 'project_app', 'technology_postgresql', 'technology_django']

3. Developer Smith reported a bug in the authentication system
   Found entities: ['person_developer', 'person_smith', 'project_system', 'concept_bug']

4. The API service needs optimization for better performance
   Found entities: ['project_service', 'project_api']

5. John from the team fixed the timeout error in the PostgreSQL database
   Found entities: ['person_john', 'technology_database', 'technology_postgresql', 'concept_error', 'concept_timeout']

6. The Django app is now working properly after Smith's bug fix
   Found entities: ['person_smith', 'project_app', 'technology_django', 'concept_bug']

=== Entity Storage Summary ===
- user (person): 1 mentions, importance: 1.00
- app (project): 3 mentions, importance: 1.20
- database (technology): 2 mentions, importance: 1.10
- issue (concept): 1 mentions, importance: 1.00
- customer (person): 1 mentions, importance: 1.00
- postgresql (technology): 2 mentions, importance: 1.10
- django (technology): 2 mentions, importance: 1.10
- developer (person): 1 mentions, importance: 1.00
- smith (person): 2 mentions, importance: 1.10
- system (project): 1 mentions, importance: 1.00
- bug (concept): 2 mentions, importance: 1.10
- service (project): 1 mentions, importance: 1.00
- api (project): 1 mentions, importance: 1.00
- john (person): 1 mentions, importance: 1.00
- error (concept): 1 mentions, importance: 1.00
- timeout (concept): 1 mentions, importance: 1.00

=== Query Examples ===
Query: 'Help optimize the database performance'
Relevant entities:
  - database (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - app (project) - mentioned 3 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - postgresql (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - user (person) - mentioned 1 times
    Recent context: The user mentioned their app has database performance issues
  - issue (concept) - mentioned 1 times
    Recent context: The user mentioned their app has database performance issues

Query: 'Who fixed the authentication bug?'
Relevant entities:
  - bug (concept) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - app (project) - mentioned 3 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - database (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - smith (person) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - postgresql (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database

Query: 'What technology does the app use?'
Relevant entities:
  - app (project) - mentioned 3 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - django (technology) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - database (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - postgresql (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - bug (concept) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix

Query: 'Tell me about recent errors'
Relevant entities:
  - error (concept) - mentioned 1 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database
  - app (project) - mentioned 3 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - django (technology) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - bug (concept) - mentioned 2 times
    Recent context: The Django app is now working properly after Smith's bug fix
  - database (technology) - mentioned 2 times
    Recent context: John from the team fixed the timeout error in the PostgreSQL database

=== Entity Network Example ===
Entity: smith (person)
Related entities:
  - reported: bug (concept)
