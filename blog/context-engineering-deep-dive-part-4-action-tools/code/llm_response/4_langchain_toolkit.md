LangChain Toolkit Approach

==================================================
=== LangChain SQL Toolkit Demo ===

Available tools:
  • execute_sql_query: Execute a read-only SQL query on the database
  • get_database_schema: Get the schema of all tables in the database

==================================================

1. Getting database schema:

Database Schema:
==================================================

Table: customers
  - id (INTEGER)
  - name (TEXT)
  - email (TEXT)
  - country (TEXT)
  - total_spent (REAL)

Table: orders
  - id (INTEGER)
  - customer_id (INTEGER)
  - product (TEXT)
  - amount (REAL)
  - order_date (DATE)


==================================================

2. Executing safe queries:


Query: SELECT * FROM customers WHERE country = 'USA'
Columns: id, name, email, country, total_spent
--------------------------------------------------
1 | Alice Johnson | alice@example.com | USA | 1500.0
4 | Diana Prince | diana@example.com | USA | 3200.0

(Showing 2 of 2 results)
--------------------------------------------------

Query: SELECT COUNT(*) as total_orders FROM orders
Columns: total_orders
--------------------------------------------------
5

(Showing 1 of 1 results)
--------------------------------------------------

Query: SELECT c.name, SUM(o.amount) as total FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id
Columns: name, total
--------------------------------------------------
Alice Johnson | 1250.0
Bob Smith | 800.0
Charlie Brown | 150.0
Diana Prince | 2500.0

(Showing 4 of 4 results)
--------------------------------------------------


=== LLM Integration Demo ===


Question: What are the top 3 customers by total spent?
Generated SQL: ```sql
SELECT name, total_spent 
FROM customers 
ORDER BY total_spent DESC 
LIMIT 3;
```
Result:
Error executing query: near "```sql
SELECT name, total_spent 
FROM customers 
ORDER BY total_spent DESC 
LIMIT 3;
```": syntax error
--------------------------------------------------

Question: How many orders do we have in total?
Generated SQL: ```sql
SELECT COUNT(*) AS total_orders FROM orders;
```
Result:
Error executing query: near "```sql
SELECT COUNT(*) AS total_orders FROM orders;
```": syntax error
--------------------------------------------------

Question: Show me all customers from the USA
Generated SQL: ```sql
SELECT * FROM customers WHERE country = 'USA';
```
Result:
Error executing query: near "```sql
SELECT * FROM customers WHERE country = 'USA';
```": syntax error
--------------------------------------------------
