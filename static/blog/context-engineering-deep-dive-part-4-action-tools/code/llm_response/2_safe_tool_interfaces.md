Safe Tool Interfaces Demo

==================================================
=== Database Query Safety Demo ===


Testing: SELECT * FROM users WHERE age > 25
⚠️  Auto-added LIMIT 1000 to prevent large result sets
✅ Query validated: SELECT * FROM users WHERE age > 25 LIMIT 1000

Testing: SELECT COUNT(*) FROM orders
⚠️  Auto-added LIMIT 1000 to prevent large result sets
✅ Query validated: SELECT COUNT(*) FROM orders LIMIT 1000

Testing: DELETE FROM users WHERE id = 1
✅ Correctly blocked: 1 validation error for DatabaseQuery
query
  Value error, ❌ Destructive operation 'DELETE' not allowed [type=value_error, input_value='DELETE FROM users WHERE id = 1', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error

Testing: DROP TABLE users
✅ Correctly blocked: 1 validation error for DatabaseQuery
query
  Value error, ❌ Destructive operation 'DROP' not allowed [type=value_error, input_value='DROP TABLE users', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error

Testing: UPDATE users SET admin = true
✅ Correctly blocked: 1 validation error for DatabaseQuery
query
  Value error, ❌ Destructive operation 'UPDATE' not allowed [type=value_error, input_value='UPDATE users SET admin = true', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error

Testing: SELECT * FROM users; DELETE FROM orders
✅ Correctly blocked: 1 validation error for DatabaseQuery
query
  Value error, ❌ Destructive operation 'DELETE' not allowed [type=value_error, input_value='SELECT * FROM users; DELETE FROM orders', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/value_error

Testing: select * from products
⚠️  Auto-added LIMIT 1000 to prevent large result sets
✅ Query validated: select * from products LIMIT 1000


=== Defense-in-Depth Pattern ===

Executing safe query:
✅ Input validation passed
📝 Audit log: Executing DatabaseQuery
⏱️  Timeout protection active
🔒 Executing in sandbox environment

🔒 Executing query on staging database:
   Query: SELECT name, email FROM users LIMIT 10
   Timeout: 30s
   Status: Would execute with read-only credentials


Executing file operation:
✅ Input validation passed
📝 Audit log: Executing FileOperation
⏱️  Timeout protection active
🔒 Executing in sandbox environment
