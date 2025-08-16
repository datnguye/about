Constraint-Based Prompting Demo

=== CONSTRAINT ADHERENCE TEST ===

--- Migration Script Generation ---
Generated Migration:
[94m```sql
-- ==========================================================
-- Migration: Add user_preferences table with theme and
-- notification_settings columns, and index on user_id
-- Author: <Your Name>
-- Date: <YYYY-MM-DD>
-- Estimated total migration time: 0.5 s
-- ==========================================================

-- ----------------------------------------------------------
-- Transaction 1: Create the user_preferences table
-- Estimated time: 0.1 s
-- ----------------------------------------------------------
BEGIN;
CREATE TABLE IF NOT EXISTS user_preferences (
    id              serial PRIMARY KEY,
    user_id         integer NOT NULL
);
COMMIT;

-- ----------------------------------------------------------
-- Transaction 2: Add theme and notification_settings columns
-- Estimated time: 0.1 s
-- ----------------------------------------------------------
BEGIN;
ALTER TABLE user_preferences
    ADD COLUMN IF NOT EXISTS theme text;
ALTER TABLE user_preferences
    ADD COLUMN IF NOT EXISTS notification_settings jsonb;
COMMIT;

-- ----------------------------------------------------------
-- Transaction 3: Create index on user_id
-- Estimated time: 0.05 s
-- ----------------------------------------------------------
BEGIN;
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id
    ON user_preferences(user_id);
COMMIT;

-- ==========================================================
-- ROLLBACK SCRIPT
-- ----------------------------------------------------------
-- Estimated time: 0.2 s
-- ----------------------------------------------------------
BEGIN;
-- 1. Backup the table before dropping it
CREATE TABLE IF NOT EXISTS user_preferences_backup AS TABLE user_preferences;

-- 2. Drop the index (if it exists)
DROP INDEX IF EXISTS idx_user_preferences_user_id;

-- 3. Drop the user_preferences table (after backup)
DROP TABLE IF EXISTS user_preferences;
COMMIT;
```[0m
--------------------------------------------------

--- Security Constrained Generator ---

Request: Find users by email address

[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new[0m
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

Error: litellm.APIError: APIError: OpenrouterException - Unable to get json response - Expecting value: line 309 column 1 (char 1694), Original Response: 
         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         


Request: Get user login history
Generated Query:
[94m-- Validate input parameters: :user_id, :max_results, :retention_date, :current_user
-- SQL injection prevention: use parameterized queries only

INSERT INTO audit_log (user_id, accessed_by, access_time, query_text)
VALUES (:user_id, :current_user, CURRENT_TIMESTAMP,
        'SELECT user_id, login_time, CONCAT(SUBSTRING(ip_address,1,7),''***''), device, location FROM login_history WHERE user_id = :user_id AND login_time >= :retention_date ORDER BY login_time DESC LIMIT :max_results');

SELECT user_id,
       login_time,
       CONCAT(SUBSTRING(ip_address,1,7),''***'') AS masked_ip_address,
       device,
       location
FROM login_history
/*+ INDEX(login_history idx_user_login_time) */
WHERE user_id = :user_id
  AND login_time >= :retention_date
ORDER BY login_time DESC
LIMIT :max_results;[0m

Request: Search products by name

[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new[0m
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

Error: litellm.APIError: APIError: OpenrouterException - Unable to get json response - Expecting value: line 481 column 1 (char 2640), Original Response: 
         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

--------------------------------------------------

--- Performance Constrained Generator ---

Request: Get top selling products

[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new[0m
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

Error: litellm.APIError: APIError: OpenrouterException - Unable to get json response - Expecting value: line 203 column 1 (char 1111), Original Response: 
         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         


Request: Find customers with high order values

[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new[0m
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

Error: litellm.APIError: APIError: OpenrouterException - Unable to get json response - Expecting value: line 471 column 1 (char 2585), Original Response: 
         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         

         


Request: Generate monthly sales report
Generated Query:
[94m```sql
/* TAG: monthly_sales_report */
/* ESTIMATED_ROW_COUNT: 5000 */
/* SET statement_timeout = 30000 */
/* LOG_SLOW_QUERY_WARNING */
/* EXECUTION_PLAN: will be displayed by the database engine */

SELECT
    DATE_TRUNC('month', s.sale_date) AS sale_month,
    SUM(s.amount) AS total_sales,
    COUNT(*) AS total_transactions,
    p.category AS product_category
FROM
    sales s
    JOIN products p ON s.product_id = p.id
/*+ READ_REPLICA */
/*+ INDEX(s sales_date_amount_idx) */
WHERE
    s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY
    sale_month,
    p.category
ORDER BY
    sale_month DESC
LIMIT 1000;
```[0m

================================================================================

=== CONSTRAINT ENFORCEMENT DEMO ===

Testing format constraints:

Request: Count active users
JSON Output:
[94m{
  "query": "-- query type: count active users\nSELECT COUNT(*) FROM users WHERE active = 1;",
  "explanation": "Counts the number of users marked as active.",
  "estimated_cost": "low",
  "confidence": 0.95
}[0m
✓ Valid JSON format

Request: Find expensive orders
JSON Output:
[94m{
  "query": "-- select SELECT order_id FROM orders WHERE total_amount > 1000;",
  "explanation": "Select orders with total_amount > 1000",
  "estimated_cost": "low",
  "confidence": 0.95
}[0m
✓ Valid JSON format

Request: List product categories
JSON Output:
[94m{
  "query": "-- query: list product categories\nSELECT DISTINCT category FROM products;",
  "explanation": "Retrieves distinct product categories from the products table.",
  "estimated_cost": "low",
  "confidence": 0.95
}[0m
✓ Valid JSON format

================================================================================

=== BOUNDARY CONDITIONS TEST ===

Challenging request: Search all text fields for any mention of a user-provided term
Response:
[94m```sql
-- Requires a full‑text index on (Column1, Column2, Column3, Column4)
SELECT *
FROM MyTable
WHERE CONTAINS((Column1, Column2, Column3, Column4), @SearchTerm);
```
[0m
----------------------------------------
Challenging request: Generate a dynamic report with user-defined columns and filters
Response:
[94m```sql
-- Static query for a dynamic report with user‑defined filters
-- Assumes the following indexes exist:
--   CREATE INDEX idx_users_status ON users(status);
--   CREATE INDEX idx_users_created_at ON users(created_at);
--   CREATE INDEX idx_users_email ON users(email);

SELECT
    u.id,
    u.name,
    u.email,
    u.created_at,
    u.status
FROM
    users u
WHERE
    u.status = @status
    AND u.created_at >= @start_date
    AND u.created_at <= @end_date
    AND u.email LIKE @email_pattern
ORDER BY
    u.created_at DESC
LIMIT 1000;
```[0m
----------------------------------------
Challenging request: Find similar records using fuzzy matching across all tables
Response:
[94mI’m sorry, but I can’t comply with that request.[0m
----------------------------------------
