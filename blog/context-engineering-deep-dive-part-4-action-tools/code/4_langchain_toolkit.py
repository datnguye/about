"""
Example 4: LangChain Toolkit Approach
Demonstrates building safe SQL toolkits with LangChain
"""

import sqlite3

from dotenv import load_dotenv
from langchain.tools import Tool, StructuredTool
from litellm import completion
from os import getenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class SQLQueryInput(BaseModel):
    """Input schema for SQL query tool"""

    query: str = Field(description="SQL query to execute")
    limit: int = Field(default=10, description="Maximum number of results")


def create_sample_database():
    """Create a sample SQLite database for demonstration"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create sample tables
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            country TEXT,
            total_spent REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product TEXT,
            amount REAL,
            order_date DATE
        )
    """)

    # Insert sample data
    customers = [
        (1, "Alice Johnson", "alice@example.com", "USA", 1500.00),
        (2, "Bob Smith", "bob@example.com", "UK", 2300.00),
        (3, "Charlie Brown", "charlie@example.com", "Canada", 1800.00),
        (4, "Diana Prince", "diana@example.com", "USA", 3200.00),
        (5, "Eve Wilson", "eve@example.com", "Australia", 2100.00),
    ]

    orders = [
        (1, 1, "Laptop", 1200.00, "2024-01-15"),
        (2, 1, "Mouse", 50.00, "2024-01-20"),
        (3, 2, "Monitor", 800.00, "2024-01-18"),
        (4, 3, "Keyboard", 150.00, "2024-01-22"),
        (5, 4, "Desktop PC", 2500.00, "2024-01-25"),
    ]

    cursor.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers
    )
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
    conn.commit()

    return conn


class SafeSQLToolkit:
    """Safe SQL toolkit with multiple safety layers"""

    def __init__(self, connection):
        self.conn = connection
        self.query_history = []
        self.max_rows = 100

    def validate_query(self, query: str) -> bool:
        """Validate query safety"""
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
        query_upper = query.upper()

        for keyword in dangerous_keywords:
            if keyword in query_upper:
                raise ValueError(f"Dangerous operation '{keyword}' not allowed")

        return True

    def execute_query(self, query: str, limit: int = 10) -> str:
        """Execute SQL query with safety checks"""
        try:
            # Validate query
            self.validate_query(query)

            # Add limit if not present
            if "LIMIT" not in query.upper():
                query = f"{query} LIMIT {min(limit, self.max_rows)}"

            # Log query
            self.query_history.append(query)

            # Execute
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()

            # Format results
            if results:
                columns = [description[0] for description in cursor.description]
                output = f"Columns: {', '.join(columns)}\n"
                output += "-" * 50 + "\n"
                for row in results[:10]:  # Limit display
                    output += " | ".join(str(val) for val in row) + "\n"
                output += f"\n(Showing {min(len(results), 10)} of {len(results)} results)"
            else:
                output = "No results found"

            return output

        except Exception as e:
            return f"Error executing query: {str(e)}"

    def get_schema(self) -> str:
        """Get database schema information"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = cursor.fetchall()

        schema_info = "Database Schema:\n" + "=" * 50 + "\n"

        for (table,) in tables:
            schema_info += f"\nTable: {table}\n"
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            for col in columns:
                schema_info += f"  - {col[1]} ({col[2]})\n"

        return schema_info


def create_langchain_tools(toolkit: SafeSQLToolkit):
    """Create LangChain tools from toolkit"""

    # Query execution tool
    query_tool = StructuredTool.from_function(
        func=toolkit.execute_query,
        name="execute_sql_query",
        description="Execute a read-only SQL query on the database",
        args_schema=SQLQueryInput,
        return_direct=False,
        handle_tool_error=True,
    )

    # Schema inspection tool
    schema_tool = Tool(
        name="get_database_schema",
        func=toolkit.get_schema,
        description="Get the schema of all tables in the database",
    )

    return [query_tool, schema_tool]


def demonstrate_toolkit_usage():
    """Demonstrate using the SQL toolkit"""
    print("=== LangChain SQL Toolkit Demo ===\n")

    # Create sample database and toolkit
    conn = create_sample_database()
    toolkit = SafeSQLToolkit(conn)

    # Create tools
    tools = create_langchain_tools(toolkit)

    print("Available tools:")
    for tool in tools:
        print(f"  • {tool.name}: {tool.description}")

    print("\n" + "=" * 50 + "\n")

    # Test schema tool
    print("1. Getting database schema:\n")
    schema_tool = tools[1]
    schema = schema_tool.func()
    print(schema)

    print("\n" + "=" * 50 + "\n")

    # Test query tool
    print("2. Executing safe queries:\n")
    query_tool = tools[0]

    test_queries = [
        "SELECT * FROM customers WHERE country = 'USA'",
        "SELECT COUNT(*) as total_orders FROM orders",
        "SELECT c.name, SUM(o.amount) as total FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id",
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = query_tool.func(query=query, limit=5)
        print(result)
        print("-" * 50)


def demonstrate_llm_integration():
    """Show how to integrate with LLM for natural language queries"""
    print("\n\n=== LLM Integration Demo ===\n")

    # Create sample database and toolkit
    conn = create_sample_database()
    toolkit = SafeSQLToolkit(conn)

    def natural_language_to_sql(question: str) -> str:
        """Convert natural language to SQL using LLM"""

        # Get schema for context
        schema = toolkit.get_schema()

        prompt = f"""Given this database schema:

{schema}

Convert this question to a SQL query:
"{question}"

Return only the SQL query, nothing else."""

        response = completion(
            model="openrouter/openai/gpt-4o-mini",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        return response.choices[0].message.content.strip()

    # Test natural language queries
    questions = [
        "What are the top 3 customers by total spent?",
        "How many orders do we have in total?",
        "Show me all customers from the USA",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")
        try:
            sql = natural_language_to_sql(question)
            print(f"Generated SQL: {sql}")
            result = toolkit.execute_query(sql)
            print(f"Result:\n{result}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 50)


if __name__ == "__main__":
    print("LangChain Toolkit Approach\n")
    print("=" * 50)

    demonstrate_toolkit_usage()
    demonstrate_llm_integration()
