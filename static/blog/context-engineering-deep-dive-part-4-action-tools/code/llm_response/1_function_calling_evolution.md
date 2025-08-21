Function Calling Evolution Demo

==================================================
=== Old Way: JSON Parsing ===

Raw response:
{
  "action": "optimize_query",
  "query": "SELECT * FROM users WHERE age > 25",
  "suggestions": ["Add index on age column", "Use specific columns instead of *"]
}

✅ Successfully parsed JSON:
{
  "action": "optimize_query",
  "query": "SELECT * FROM users WHERE age > 25",
  "suggestions": [
    "Add index on age column",
    "Use specific columns instead of *"
  ]
}

=== Modern Way: Function Calling ===

✅ Function called: optimize_query
Arguments received:
{
  "query": "SELECT * FROM users WHERE age > 25",
  "suggestions": [
    "Consider selecting only the columns you need instead of using SELECT *",
    "Create an index on the age column to speed up the WHERE clause",
    "If you have a large dataset, consider pagination to limit the number of rows returned."
  ]
}

Query to optimize: SELECT * FROM users WHERE age > 25
Target DB: Not specified
Suggestions:
  1. Consider selecting only the columns you need instead of using SELECT *
  2. Create an index on the age column to speed up the WHERE clause
  3. If you have a large dataset, consider pagination to limit the number of rows returned.
