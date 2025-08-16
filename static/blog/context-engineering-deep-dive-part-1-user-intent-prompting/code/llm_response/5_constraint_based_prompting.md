Constraint-Based Prompting Demo

=== CONSTRAINT ADHERENCE TEST ===

--- Migration Script Generation ---
Generated Migration:
[94m```sql
-- =========================================================
-- Migration: Add user_preferences table, columns, and index
-- Author: <Your Name>
-- Date: 2025-08-16
-- =========================================================

-- ==============================
-- Transaction 1: Create table
-- Estimated time: 0.10 s
-- ==============================
BEGIN;
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id BIGINT PRIMARY KEY,
    theme VARCHAR(50),
    notification_settings JSONB
);
COMMIT;

-- ==============================
-- Transaction 2: Add column "theme"
-- Estimated time: 0.05 s
-- ==============================
BEGIN;
ALTER TABLE user_preferences
    ADD COLUMN IF NOT EXISTS theme VARCHAR(50);
COMMIT;

-- ==============================
-- Transaction 3: Add column "notification_settings"
-- Estimated time: 0.05 s
-- ==============================
BEGIN;
ALTER TABLE user_preferences
    ADD COLUMN IF NOT EXISTS notification_settings JSONB;
COMMIT;

-- ==============================
-- Transaction 4: Create index
-- Estimated time: 0.05 s
-- ==============================
BEGIN;
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id
    ON user_preferences(user_id);
COMMIT;

-- =========================================================
-- Rollback script (to revert the migration)
-- Estimated time: 0.20 s
-- =========================================================
BEGIN;
    -- Drop index if it exists
    DROP INDEX IF EXISTS idx_user_preferences_user_id;

    -- Drop columns if they exist
    ALTER TABLE user_preferences DROP COLUMN IF EXISTS theme;
    ALTER TABLE user_preferences DROP COLUMN IF EXISTS notification_settings;

    -- Backup the table before dropping it
    CREATE TABLE backup_user_preferences AS TABLE user_preferences;

    -- Drop the table if it exists
    DROP TABLE IF EXISTS user_preferences;
COMMIT;
```[0m
--------------------------------------------------

--- Security Constrained Generator ---

Request: Find users by email address
Generated Query:
[94m-- SQL Injection Prevention: Use parameterized query with placeholder $1
-- Input validation should be performed in the application layer (e.g., regex for email format)

WITH audit_log AS (
    INSERT INTO user_access_audit (
        user_id,
        access_time,
        accessed_by,
        query_type
    )
    VALUES (
        NULL,                     -- NULL indicates system-initiated audit
        CURRENT_TIMESTAMP,
        'admin',                  -- user_role from context
        'SELECT_BY_EMAIL'
    )
    RETURNING audit_id
)
SELECT
    u.id,
    u.name,
    CONCAT(LEFT(u.email, 3), '****', RIGHT(u.email, 4)) AS masked_email,
    u.created_at,
    a.audit_id
FROM
    users u
    JOIN audit_log a ON 1=1
/*+ INDEX(u idx_users_email) */   -- Hint to use index on email column
WHERE
    u.email = $1
LIMIT 100;   -- Respect max_results from context

/* Data retention policy: audit records older than 90 days are purged by a scheduled job. */
[0m

Request: Get user login history
Generated Query:
[94m```sql
CREATE PROCEDURE dbo.GetUserLoginHistory
    @UserId    INT,
    @StartDate DATETIME,
    @EndDate   DATETIME
AS
BEGIN
    SET NOCOUNT ON;

    /*--------------------------------------------------------------
     * SQL Injection Prevention:
     *   - Only parameterized queries are used.
     *   - No dynamic SQL or string concatenation in WHERE clauses.
     *--------------------------------------------------------------*/

    /* Validate input parameters */
    IF @UserId IS NULL OR @StartDate IS NULL OR @EndDate IS NULL
    BEGIN
        RAISERROR('Invalid input parameters', 16, 1);
        RETURN;
    END

    IF @StartDate > @EndDate
    BEGIN
        RAISERROR('StartDate must be less than or equal to EndDate', 16, 1);
        RETURN;
    END

    /* Log data access attempt (audit trail) */
    INSERT INTO dbo.audit_log (user_id, action, action_timestamp, ip_address)
    VALUES (@UserId,
            'GetUserLoginHistory',
            GETDATE(),
            CONNECTIONPROPERTY('client_net_address'));

    /* Retrieve login history with masking and retention filter */
    SELECT TOP (100)
        lh.user_id,
        lh.login_time,
        CONCAT(
            SUBSTRING(lh.ip_address,
                      1,
                      CHARINDEX('.', lh.ip_address, CHARINDEX('.', lh.ip_address)+1)-1),
            '.***.***') AS masked_ip,
        lh.device,
        lh.location
    FROM dbo.login_history lh WITH (INDEX(idx_user_login_time))
    WHERE lh.user_id = @UserId
      AND lh.login_time BETWEEN @StartDate AND @EndDate
      AND lh.login_time >= DATEADD(day, -365, GETDATE())   -- retention policy
    ORDER BY lh.login_time DESC;
END
```[0m
--------------------------------------------------

--- Performance Constrained Generator ---

Request: Get top selling products
Generated Query:
[94m```sql
/* TAG: top_selling_products
   ESTIMATED_ROWS: 5000
   LOG_SLOW_QUERY
   Execution plan: (will be generated by the optimizer)
   /*+ READ_REPLICA MAX_EXECUTION_TIME(30000) INDEX(sales sales_product_id_idx) INDEX(products products_product_id_idx) */
SELECT
    p.product_id,
    p.product_name,
    SUM(s.quantity) AS total_quantity
FROM
    sales /*+ INDEX(sales sales_product_id_idx) */ s
JOIN
    products /*+ INDEX(products products_product_id_idx) */ p
    ON s.product_id = p.product_id
WHERE
    s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY
    p.product_id,
    p.product_name
ORDER BY
    total_quantity DESC
LIMIT 1000;
```[0m

Request: Find customers with high order values
Generated Query:
[94m```sql
/* TAG: high_order_value_report
   ESTIMATED ROWS: 500
   LOG_SLOW_QUERY_WARNING
   MAX_EXECUTION_TIME(30000) -- 30 seconds
   READ_REPLICA
   INDEX(orders idx_orders_customer_id_date_value)
*/
SELECT
    c.customer_id,
    c.customer_name,
    SUM(o.order_value) AS total_order_value,
    COUNT(o.order_id) AS order_count
FROM
    customers c
JOIN
    orders o
    ON c.customer_id = o.customer_id
WHERE
    o.order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND o.order_value > 1000
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY
    total_order_value DESC
LIMIT 1000;

/* Execution plan:
   1. Use covering index idx_orders_customer_id_date_value on orders to filter by order_date and order_value.
   2. Join customers using primary key on customer_id.
   3. Aggregate results in memory (hash aggregation).
   4. Sort by total_order_value and limit to 1000 rows.
*/
```[0m

Request: Generate monthly sales report
Generated Query:
[94m```sql
/* TAG: monthly_sales_report */
/* ESTIMATED ROWS: 200 */
/* LOG_SLOW_QUERY_WARNING */
/*+ READ_REPLICA MAX_EXECUTION_TIME(30000) */

/* Using covering index sales_idx_date_amount_product on sales(sale_date, amount, product_id) */
/* Using index products_idx_id on products(id) */
/* Using index customers_idx_id on customers(id) */

SELECT
    DATE_TRUNC('month', s.sale_date) AS sale_month,
    p.name AS product_name,
    c.region AS customer_region,
    SUM(s.amount) AS total_sales,
    COUNT(*) AS sales_count
FROM
    sales s
JOIN
    products p ON s.product_id = p.id
JOIN
    customers c ON s.customer_id = c.id
WHERE
    s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY
    sale_month, p.name, c.region
ORDER BY
    sale_month DESC
LIMIT 1000;

/* Execution Plan: (to be generated by optimizer) */
```[0m

================================================================================

=== CONSTRAINT ENFORCEMENT DEMO ===

Testing format constraints:

Request: Count active users
JSON Output:
[94m{
  "query": "-- type: count\nSELECT COUNT(*) FROM users WHERE status = 'active';",
  "explanation": "Counts all users marked as active.",
  "estimated_cost": "low",
  "confidence": 0.95
}[0m
✓ Valid JSON format

Request: Find expensive orders
JSON Output:
[94m{
  "query": "-- type: select\nSELECT * FROM orders WHERE total_amount > 1000;",
  "explanation": "Select orders with total_amount greater than 1000",
  "estimated_cost": "low",
  "confidence": 0.95
}[0m
✓ Valid JSON format

Request: List product categories
JSON Output:
[94m{
  "query": "-- query: list product categories\nSELECT DISTINCT category\nFROM products;\n",
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
-- Assumes a full‑text index exists on (Column1, Column2, Column3) in dbo.MyTable

CREATE PROCEDURE dbo.SearchAllTextFields
    @searchTerm NVARCHAR(4000)   -- validated by the caller
AS
BEGIN
    SET NOCOUNT ON;

    SELECT *
    FROM dbo.MyTable
    WHERE CONTAINS((Column1, Column2, Column3), @searchTerm);
END;
```[0m
----------------------------------------
Challenging request: Generate a dynamic report with user-defined columns and filters
Response:
[94m```sql
-- Assumes a composite covering index named idx_All on (Col1, Col2, Col3)
CREATE PROCEDURE dbo.GetDynamicReport
    @IncludeCol1 BIT = 0,
    @IncludeCol2 BIT = 0,
    @IncludeCol3 BIT = 0,
    @FilterCol1 INT      = NULL,
    @FilterCol2 VARCHAR(50) = NULL,
    @FilterCol3 DATE     = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        CASE WHEN @IncludeCol1 = 1 THEN t.Col1 END AS Col1,
        CASE WHEN @IncludeCol2 = 1 THEN t.Col2 END AS Col2,
        CASE WHEN @IncludeCol3 = 1 THEN t.Col3 END AS Col3
    FROM dbo.MyTable t
    WITH (INDEX(idx_All))
    WHERE (@FilterCol1 IS NULL OR t.Col1 = @FilterCol1)
      AND (@FilterCol2 IS NULL OR t.Col2 = @FilterCol2)
      AND (@FilterCol3 IS NULL OR t.Col3 = @FilterCol3);
END
```[0m
----------------------------------------
Challenging request: Find similar records using fuzzy matching across all tables
Response:
[94m```sql
-- Assumes full‑text indexes exist on the searched columns
SELECT 'customers' AS source_table, id, name
FROM customers
WHERE CONTAINS(name, @searchTerm)

UNION ALL

SELECT 'orders' AS source_table, id, order_number
FROM orders
WHERE CONTAINS(order_number, @searchTerm)

UNION ALL

SELECT 'products' AS source_table, id, product_name
FROM products
WHERE CONTAINS(product_name, @searchTerm);
```
[0m
----------------------------------------
