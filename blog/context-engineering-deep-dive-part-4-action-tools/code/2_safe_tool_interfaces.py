"""
Example 2: Building Safe Tool Interfaces
Demonstrates multiple layers of safety for LLM tools
"""

import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class DatabaseQuery(BaseModel):
    """Tool for read-only database queries with multiple safety layers"""

    query: str = Field(description="SQL query to execute")
    database: Literal["staging", "analytics"] = Field(
        default="staging", description="Target database (prod not available)"
    )
    timeout_seconds: int = Field(default=30, le=60, description="Query timeout")

    @field_validator("query")
    def validate_query(cls, v):
        """Multi-layer query validation"""
        # Layer 1: No destructive operations
        dangerous_keywords = [
            "DELETE",
            "UPDATE",
            "DROP",
            "ALTER",
            "TRUNCATE",
            "INSERT",
            "CREATE",
            "REPLACE",
        ]
        query_upper = v.upper()

        for keyword in dangerous_keywords:
            if re.search(r"\b" + keyword + r"\b", query_upper):
                raise ValueError(f"❌ Destructive operation '{keyword}' not allowed")

        # Layer 2: Must be a SELECT query
        if not query_upper.strip().startswith("SELECT"):
            raise ValueError("❌ Only SELECT queries allowed")

        # Layer 3: Force LIMIT if not present
        if "LIMIT" not in query_upper:
            v = f"{v.rstrip(';')} LIMIT 1000"
            print("⚠️  Auto-added LIMIT 1000 to prevent large result sets")

        return v

    def execute(self):
        """Execute with additional runtime checks"""
        print(f"\n🔒 Executing query on {self.database} database:")
        print(f"   Query: {self.query}")
        print(f"   Timeout: {self.timeout_seconds}s")
        print("   Status: Would execute with read-only credentials")
        return "Query executed successfully (simulated)"


class FileOperation(BaseModel):
    """Safe file operation tool"""

    operation: Literal["read", "list"] = Field(description="Operation type")
    path: str = Field(description="File or directory path")
    max_size_mb: int = Field(default=10, le=100, description="Max file size in MB")

    @field_validator("path")
    def validate_path(cls, v):
        """Path traversal prevention"""
        # Remove any path traversal attempts
        if "../" in v or "..\\" in v:
            raise ValueError("❌ Path traversal detected")

        # Check for absolute paths trying to escape
        if v.startswith("/etc") or v.startswith("/sys"):
            raise ValueError("❌ Access to system directories not allowed")

        return v


def demonstrate_query_safety():
    """Show query validation in action"""
    print("=== Database Query Safety Demo ===\n")

    test_queries = [
        # Safe queries
        ("SELECT * FROM users WHERE age > 25", True),
        ("SELECT COUNT(*) FROM orders", True),
        # Dangerous queries
        ("DELETE FROM users WHERE id = 1", False),
        ("DROP TABLE users", False),
        ("UPDATE users SET admin = true", False),
        # Edge cases
        ("SELECT * FROM users; DELETE FROM orders", False),
        ("select * from products", True),  # Case insensitive
    ]

    for query_str, should_pass in test_queries:
        print(f"\nTesting: {query_str}")
        try:
            db_query = DatabaseQuery(query=query_str)
            if should_pass:
                print(f"✅ Query validated: {db_query.query}")
            else:
                print("⚠️  Unexpected pass - query should have been blocked")
        except ValueError as e:
            if not should_pass:
                print(f"✅ Correctly blocked: {e}")
            else:
                print(f"❌ Unexpected block: {e}")


def demonstrate_defense_layers():
    """Show multiple layers of defense"""
    print("\n\n=== Defense-in-Depth Pattern ===\n")

    class ToolExecutor:
        """Production tool executor with multiple safety layers"""

        def __init__(self):
            self.execution_count = 0
            self.rate_limit = 5

        def execute(self, tool: BaseModel):
            """Execute tool with all safety layers"""

            # Layer 1: Rate limiting
            self.execution_count += 1
            if self.execution_count > self.rate_limit:
                raise Exception(f"🛑 Rate limit exceeded ({self.rate_limit} calls)")

            # Layer 2: Input validation (handled by Pydantic)
            print("✅ Input validation passed")

            # Layer 3: Audit logging
            print(f"📝 Audit log: Executing {tool.__class__.__name__}")

            # Layer 4: Timeout wrapper (simulated)
            print("⏱️  Timeout protection active")

            # Layer 5: Sandboxing (simulated)
            print("🔒 Executing in sandbox environment")

            # Execute
            if hasattr(tool, "execute"):
                return tool.execute()

    executor = ToolExecutor()

    # Test safe query
    safe_query = DatabaseQuery(query="SELECT name, email FROM users LIMIT 10")
    print("Executing safe query:")
    executor.execute(safe_query)

    # Test file operation
    print("\n\nExecuting file operation:")
    file_op = FileOperation(operation="read", path="./config.json")
    executor.execute(file_op)


if __name__ == "__main__":
    print("Safe Tool Interfaces Demo\n")
    print("=" * 50)

    demonstrate_query_safety()
    demonstrate_defense_layers()