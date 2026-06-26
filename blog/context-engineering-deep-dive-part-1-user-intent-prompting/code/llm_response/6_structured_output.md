Structured Output Demo

=== BASIC EXTRACTION ===
Input: This query joins users with orders and filters by date, grouping results by region
Extracted:
[94m{
  "tables": [
    "users",
    "orders"
  ],
  "operations": [
    "join",
    "filter",
    "group by"
  ],
  "complexity": "medium",
  "estimated_runtime": 5
}[0m

================================================================================

=== STRUCTURED QUERY ANALYSIS ===

--- Analysis 1 ---
Query: SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.created_at > '2024-01-01'
        GROUP BY u.id
        HAVING order_count > 5
        ORDER BY total_spent DESC
Analysis:
[94m{
  "tables": [
    "users",
    "orders"
  ],
  "operations": [
    "SELECT",
    "LEFT JOIN",
    "WHERE",
    "GROUP BY",
    "HAVING",
    "ORDER BY",
    "COUNT",
    "SUM"
  ],
  "complexity": "medium",
  "estimated_runtime": 2,
  "potential_issues": [
    "Missing indexes on users.created_at, orders.user_id, and orders.total may slow query",
    "LEFT JOIN is unnecessary since HAVING filters out users with no orders; could use INNER JOIN",
    "SELECTing u.name without including it in GROUP BY may cause non-deterministic results in some SQL engines",
    "SUM(o.total) will be NULL if all joined orders are NULL; consider COALESCE",
    "Date literal '2024-01-01' may be affected by timezone settings"
  ],
  "optimization_suggestions": [
    "Replace LEFT JOIN with INNER JOIN to avoid unnecessary null handling",
    "Add indexes on users.created_at, orders.user_id, and orders.total to speed up filtering and aggregation",
    "Use COUNT(*) instead of COUNT(o.id) for slightly better performance",
    "Consider pre-aggregating orders in a subquery to reduce data processed in GROUP BY",
    "Use COALESCE(SUM(o.total),0) if NULL totals should be treated as zero"
  ],
  "confidence_score": 0.95
}[0m

--- Analysis 2 ---
Query: SELECT * FROM products p, categories c, orders o, order_items oi
        WHERE p.category_id = c.id
        AND oi.product_id = p.id
        AND oi.order_id = o.id
Analysis:
[94m{
  "tables": [
    "products",
    "categories",
    "orders",
    "order_items"
  ],
  "operations": [
    "SELECT",
    "FROM",
    "WHERE"
  ],
  "complexity": "low",
  "estimated_runtime": 1,
  "potential_issues": [
    "Uses implicit join syntax which can be error\u2011prone",
    "SELECT * returns all columns, causing unnecessary data transfer and possible column name collisions",
    "No filtering or LIMIT clause, may return a very large result set",
    "Missing indexes on foreign key columns (products.category_id, order_items.product_id, order_items.order_id) and primary keys",
    "No explicit JOIN syntax, making join order unclear to optimizer",
    "No use of specific columns, leading to heavier I/O"
  ],
  "optimization_suggestions": [
    "Rewrite using explicit JOIN syntax (INNER JOIN) for clarity",
    "Add indexes on products.category_id, order_items.product_id, order_items.order_id, and primary keys of referenced tables",
    "Select only required columns instead of *",
    "Add appropriate WHERE filters or LIMIT to reduce result size",
    "Consider using EXISTS or IN if applicable",
    "Use query hints or optimizer directives if supported",
    "Ensure statistics are up to date for better join ordering"
  ],
  "confidence_score": 0.9
}[0m

--- Analysis 3 ---
Query: SELECT user_id FROM sessions WHERE last_activity > NOW() - INTERVAL 1 HOUR
Analysis:
[94m{
  "tables": [
    "sessions"
  ],
  "operations": [
    "SELECT",
    "WHERE"
  ],
  "complexity": "low",
  "estimated_runtime": 1,
  "potential_issues": [
    "Potential full table scan if last_activity is not indexed",
    "No LIMIT clause may return large result set",
    "No index on last_activity may degrade performance"
  ],
  "optimization_suggestions": [
    "Add index on last_activity",
    "Add LIMIT clause if only a subset needed",
    "Use covering index on user_id and last_activity",
    "Consider partitioning sessions table by activity date"
  ],
  "confidence_score": 0.99
}[0m

================================================================================

=== STRUCTURED SECURITY AUDIT ===

--- Security Audit 1 ---
Query: SELECT * FROM users WHERE username = 'user_input'
Security Audit:
[94m{
  "vulnerability_level": "high",
  "vulnerabilities_found": [
    "SQL Injection",
    "Data Exposure"
  ],
  "sql_injection_risk": true,
  "data_exposure_risk": true,
  "recommendations": [
    "Use parameterized queries or prepared statements to avoid direct string concatenation.",
    "Specify only required columns instead of SELECT * to limit data exposure.",
    "Implement input validation and sanitization for user_input.",
    "Apply least privilege principle on database user permissions."
  ],
  "compliant_with_standards": [],
  "audit_score": "2"
}[0m

--- Security Audit 2 ---
Query: SELECT * FROM credit_cards WHERE user_id = 123
Security Audit:
[94m{
  "vulnerability_level": "medium",
  "vulnerabilities_found": [
    "SELECT * may expose unnecessary sensitive data"
  ],
  "sql_injection_risk": false,
  "data_exposure_risk": true,
  "recommendations": [
    "Specify only required columns instead of SELECT *",
    "Use parameterized queries to prevent injection",
    "Apply least privilege principle for database user",
    "Encrypt sensitive data at rest",
    "Implement proper access controls and logging"
  ],
  "compliant_with_standards": [
    "PCI-DSS",
    "OWASP Top 10"
  ],
  "audit_score": 6
}[0m

--- Security Audit 3 ---
Query: SELECT password_hash, salt FROM users WHERE email = ?
Security Audit:
[94m{
  "vulnerability_level": "medium",
  "vulnerabilities_found": [
    "Retrieval of password_hash and salt may expose sensitive data if not properly protected",
    "Potential data exposure if query results are returned to client",
    "No explicit access control or rate limiting shown"
  ],
  "sql_injection_risk": false,
  "data_exposure_risk": true,
  "recommendations": [
    "Avoid returning password_hash and salt to client; store them securely",
    "Use strong hashing algorithm with salt (e.g., bcrypt, Argon2)",
    "Ensure database credentials have least privilege",
    "Implement proper access controls and audit logging",
    "Apply rate limiting to prevent enumeration attacks",
    "Encrypt sensitive data at rest",
    "Use parameterized queries (already in place) to mitigate SQL injection"
  ],
  "compliant_with_standards": [
    "OWASP Secure Coding Practices",
    "PCI-DSS (partial compliance)"
  ],
  "audit_score": 6
}[0m

--- Security Audit 4 ---
Query: UPDATE users SET admin = 1 WHERE user_id = user_controlled_id
Security Audit:
[94m{
  "vulnerability_level": "high",
  "vulnerabilities_found": [
    "SQL injection",
    "Privilege escalation via unsanitized user_id",
    "Missing parameterization"
  ],
  "sql_injection_risk": true,
  "data_exposure_risk": true,
  "recommendations": [
    "Use parameterized queries or prepared statements",
    "Validate and sanitize user_id input",
    "Implement least privilege and role-based access control",
    "Add audit logging for privilege changes",
    "Consider using stored procedures",
    "Enforce input validation and type checking"
  ],
  "compliant_with_standards": [],
  "audit_score": 2
}[0m

================================================================================

=== STRUCTURED PERFORMANCE REPORT ===

--- Performance Report 1 ---
Query: SELECT COUNT(*) FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.created_at > '2023-01-01'
Performance Report:
[94m{
  "estimated_execution_time": "5-10 seconds",
  "resource_usage": {
    "cpu_intensive": false,
    "memory_intensive": false,
    "io_intensive": true
  },
  "scalability_concerns": [
    "Large number of rows in orders and order_items leading to join amplification",
    "Potential full table scans if indexes missing",
    "High I/O load on disk for scanning and joining",
    "Counting after join may become expensive as data grows"
  ],
  "recommended_indexes": [
    "CREATE INDEX idx_orders_created_at ON orders(created_at);",
    "CREATE INDEX idx_order_items_order_id ON order_items(order_id);",
    "CREATE INDEX idx_order_items_product_id ON order_items(product_id);",
    "CREATE INDEX idx_products_id ON products(id);"
  ],
  "alternative_approaches": [
    "SELECT COUNT(*) FROM order_items oi JOIN orders o ON oi.order_id = o.id WHERE o.created_at > '2023-01-01';",
    "Use a derived table: SELECT COUNT(*) FROM (SELECT oi.id FROM order_items oi JOIN orders o ON oi.order_id = o.id WHERE o.created_at > '2023-01-01') AS sub;",
    "Create a materialized view that pre-aggregates counts per order date and query that view instead of joining large tables;"
  ],
  "bottlenecks": [
    "Join amplification due to many order_items per order",
    "Missing indexes causing full table scans",
    "Counting after join forces processing of all joined rows"
  ],
  "optimization_priority": "high"
}[0m

--- Performance Report 2 ---
Query: SELECT u.*,
               (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count,
               (SELECT SUM(total) FROM orders WHERE user_id = u.id) as total_spent
        FROM users u
Performance Report:
[94m{
  "estimated_execution_time": "10 seconds",
  "resource_usage": {
    "cpu_intensive": false,
    "memory_intensive": false,
    "io_intensive": true
  },
  "scalability_concerns": [
    "High I/O due to correlated subqueries",
    "Scales poorly with large user and order tables",
    "Potential for long query times as data grows"
  ],
  "recommended_indexes": [
    "CREATE INDEX idx_orders_user_id ON orders(user_id);",
    "CREATE INDEX idx_orders_user_id_total ON orders(user_id, total);"
  ],
  "alternative_approaches": [
    "SELECT u.*, o.order_count, o.total_spent FROM users u LEFT JOIN (SELECT user_id, COUNT(*) AS order_count, SUM(total) AS total_spent FROM orders GROUP BY user_id) o ON u.id = o.user_id;",
    "Use window functions: SELECT u.*, COUNT(*) OVER (PARTITION BY u.id) AS order_count, SUM(total) OVER (PARTITION BY u.id) AS total_spent FROM users u LEFT JOIN orders ON orders.user_id = u.id;",
    "Materialize aggregates in a separate table and update via triggers."
  ],
  "bottlenecks": [
    "Correlated subqueries causing repeated scans of orders table",
    "Missing index on orders.user_id",
    "Potential full table scans for each user"
  ],
  "optimization_priority": "high"
}[0m

--- Performance Report 3 ---
Query: SELECT * FROM logs
        WHERE message LIKE '%error%'
        AND created_at BETWEEN '2024-01-01' AND '2024-12-31'
        ORDER BY created_at DESC
Performance Report:
[94m{
  "estimated_execution_time": "5-10 seconds",
  "resource_usage": {
    "cpu_intensive": false,
    "memory_intensive": false,
    "io_intensive": true
  },
  "scalability_concerns": [
    "Full table scans on large logs table",
    "High I/O load due to leading wildcard in LIKE",
    "Potential lock contention on ORDER BY",
    "Index fragmentation over time"
  ],
  "recommended_indexes": [
    "CREATE INDEX idx_logs_created_at ON logs(created_at DESC);",
    "CREATE FULLTEXT INDEX idx_logs_message_ft ON logs(message);",
    "CREATE INDEX idx_logs_created_at_message ON logs(created_at, message);"
  ],
  "alternative_approaches": [
    "Use full-text search instead of LIKE",
    "Partition logs table by year to reduce scan size",
    "Create a materialized view for error logs",
    "Add a computed boolean column is_error and index it"
  ],
  "bottlenecks": [
    "Leading wildcard in LIKE prevents index usage",
    "Large volume of log rows",
    "Sorting on created_at after filtering"
  ],
  "optimization_priority": "high"
}[0m

================================================================================

=== EDGE CASES TEST ===

--- Edge Case 1 ---
Input: 'Analyze this completely invalid SQL: SELECT * FROM nowhere WHERE nothing = everything'
Response:
[94m{
  "status": "error",
  "message": "Invalid SQL query: SELECT * FROM nowhere WHERE nothing = everything",
  "data": null
}[0m

--- Edge Case 2 ---
Input: 'What is the meaning of life?'
Response:
[94m{
  "status": "success",
  "message": "Answer to the meaning of life.",
  "data": "The meaning of life is to seek purpose, connection growth."
}[0m

--- Edge Case 3 ---
Input: 'Generate a SQL query for something impossible'
Response:
[94m{
  "status": "error",
  "message": "Cannot generate a SQL query for an impossible task.",
  "data": null
}[0m

--- Edge Case 4 ---
Input: ''
Response:
[94m{
  "status": "success",
  "message": "No input provided",
  "data": null
}[0m

