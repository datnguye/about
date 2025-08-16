Few-Shot Learning Demo

=== ZERO-SHOT vs FEW-SHOT COMPARISON ===

Query 1: 'Find customers who spent over 1000'
--------------------------------------------------
Zero-shot result:
[94m```sql
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o          ON c.customer_id = o.customer_id
JOIN order_items oi    ON o.order_id   = oi.order_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(oi.quantity * oi.unit_price) > 1000;
```
[0m

Few-shot result:
[94mSELECT customer_id, SUM(amount) AS total_spent
FROM orders
GROUP BY customer_id
HAVING total_spent > 1000;[0m

Advanced few-shot with schema:
[94mHere’s a straightforward query that pulls all customers whose cumulative spending exceeds $1,000:

```sql
SELECT
    customer_id,
    name,
    email,
    total_spent,
    created_at
FROM
    customers
WHERE
    total_spent > 1000
ORDER BY
    total_spent DESC;
```

- **`total_spent > 1000`** filters for high‑value customers.  
- Ordering by `total_spent DESC` shows the biggest spenders first.  

Feel free to adjust the columns or add additional filters (e.g., date range, specific departments) as needed.[0m

======================================================================

Query 2: 'Get products that are running low on inventory'
--------------------------------------------------
Zero-shot result:
[94mSELECT * FROM products WHERE inventory_quantity < 10;[0m

Few-shot result:
[94mSELECT * FROM products WHERE quantity <= 10;[0m

Advanced few-shot with schema:
[94m```sql
-- Products that are running low on inventory (threshold: 10 units)
SELECT
    product_id,
    name,
    price,
    inventory_count,
    category
FROM products
WHERE inventory_count < 10
ORDER BY inventory_count ASC;
```[0m

======================================================================

Query 3: 'Show me orders from the last week that haven't shipped'
--------------------------------------------------
Zero-shot result:
[94m```sql
SELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND (ship_date IS NULL OR status <> 'shipped');
```[0m

Few-shot result:
[94mSELECT *
FROM orders
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
  AND shipped_date IS NULL;[0m

Advanced few-shot with schema:
[94m```sql
-- Orders created in the last 7 days that have not yet shipped
SELECT
    order_id,
    customer_id,
    status,
    total,
    created_at
FROM
    orders
WHERE
    created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)   -- last week
    AND shipped_at IS NULL                         -- not shipped yet
ORDER BY
    created_at DESC;
```[0m

======================================================================

Query 4: 'List employees who started this month'
--------------------------------------------------
Zero-shot result:
[94m```sql
SELECT *
FROM employees
WHERE YEAR(hire_date) = YEAR(CURRENT_DATE())
  AND MONTH(hire_date) = MONTH(CURRENT_DATE());
```[0m

Few-shot result:
[94mSELECT *
FROM employees
WHERE YEAR(start_date) = YEAR(CURDATE())
  AND MONTH(start_date) = MONTH(CURDATE());[0m

Advanced few-shot with schema:
[94m```sql
SELECT employee_id, name, department, start_date, salary
FROM employees
WHERE YEAR(start_date) = YEAR(CURDATE())
  AND MONTH(start_date) = MONTH(CURDATE());
```[0m

======================================================================

=== PATTERN LEARNING DEMO ===

--- Error Analysis Pattern ---
Input: Query times out
Output:
[94mISSUE: Query timeout | CAUSE: Missing index on frequently filtered column(s) or inefficient join causing full table scans | FIX: Add appropriate indexes (e.g., `CREATE INDEX idx_orders_customer_id ON orders(customer_id)`), rewrite the query to use EXISTS or subqueries, and ensure WHERE clauses use indexed columns.[0m

--- Code Review Pattern ---
Input: SELECT COUNT(*) FROM orders o, users u WHERE o.user_id = u.id
Output:
[94mRATING: 3/5 | ISSUES: 1) Implicit join syntax (comma join) can be confusing and is less explicit than JOIN…ON. 2) COUNT(*) counts all rows, which may double‑count if the join produces duplicate rows (e.g., if a user appears multiple times). 3) No alias for the aggregate, which can make the result set harder to read. 4) No filtering on user status (e.g., active users) – may return counts for inactive users. | IMPROVE: 1) Use explicit JOIN syntax: `FROM orders o JOIN users u ON o.user_id = u.id`. 2) If you only want to count distinct orders, use `COUNT(DISTINCT o.id)` or `COUNT(o.id)` instead of `COUNT(*)`. 3) Alias the aggregate for clarity: `SELECT COUNT(*) AS order_count`. 4) Add any necessary filters, e.g., `WHERE u.active = 1`. 5) If the intent is to count orders per user, consider adding a GROUP BY clause.[0m

