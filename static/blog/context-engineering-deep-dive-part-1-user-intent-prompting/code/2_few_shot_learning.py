"""
Few-Shot Learning: Teaching patterns through examples

This script demonstrates how providing examples dramatically improves
LLM performance compared to just giving instructions.
"""

from os import getenv

from dotenv import load_dotenv
from litellm import completion

def blue_print(text):
    """Print text in blue color"""
    print(f"\033[94m{text}\033[0m")

# Load environment variables
load_dotenv()

def zero_shot_approach(user_query: str) -> str:
    """Zero-shot: Just instructions, no examples"""

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "Extract SQL queries from natural language. Return only valid SQL."},
            {"role": "user", "content": user_query}
        ]
    )

    return response["choices"][0]["message"]["content"]

def few_shot_approach(user_query: str) -> str:
    """Few-shot: Provide examples to establish the pattern"""

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "Extract SQL queries from natural language. Return only valid SQL."},
            # Few-shot examples
            {"role": "user", "content": "Show me all users from Texas"},
            {"role": "assistant", "content": "SELECT * FROM users WHERE state = 'TX';"},
            {"role": "user", "content": "Count orders from last month"},
            {"role": "assistant", "content": "SELECT COUNT(*) FROM orders WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);"},
            {"role": "user", "content": "Find users who joined this year"},
            {"role": "assistant", "content": "SELECT * FROM users WHERE YEAR(created_at) = YEAR(CURDATE());"},
            # Actual query
            {"role": "user", "content": user_query}
        ]
    )

    return response["choices"][0]["message"]["content"]

def advanced_few_shot_with_context(user_query: str, table_schema: dict) -> str:
    """Advanced few-shot with schema context"""

    schema_info = "Available tables and columns:\n"
    for table, columns in table_schema.items():
        schema_info += f"- {table}: {', '.join(columns)}\n"

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": f"You are a SQL expert. Generate queries based on the schema.\n\n{schema_info}"
            },
            # Context-aware examples
            {"role": "user", "content": "Show high-value customers"},
            {"role": "assistant", "content": "SELECT customer_id, name, total_spent FROM customers WHERE total_spent > 10000 ORDER BY total_spent DESC;"},
            {"role": "user", "content": "Find recent orders that are still processing"},
            {"role": "assistant", "content": "SELECT order_id, customer_id, created_at FROM orders WHERE status = 'processing' AND created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY);"},
            # Actual query
            {"role": "user", "content": user_query}
        ],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]

def compare_approaches():
    """Compare zero-shot vs few-shot performance"""

    test_queries = [
        "Find customers who spent over 1000",
        "Get products that are running low on inventory",
        "Show me orders from the last week that haven't shipped",
        "List employees who started this month"
    ]

    # Mock database schema
    schema = {
        "customers": ["customer_id", "name", "email", "total_spent", "created_at"],
        "products": ["product_id", "name", "price", "inventory_count", "category"],
        "orders": ["order_id", "customer_id", "status", "total", "created_at", "shipped_at"],
        "employees": ["employee_id", "name", "department", "start_date", "salary"]
    }

    print("=== ZERO-SHOT vs FEW-SHOT COMPARISON ===\n")

    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: '{query}'")
        print("-" * 50)

        # Zero-shot
        print("Zero-shot result:")
        try:
            zero_result = zero_shot_approach(query)
            blue_print(zero_result)
        except Exception as e:
            print(f"Error: {e}")

        print("\nFew-shot result:")
        try:
            few_result = few_shot_approach(query)
            blue_print(few_result)
        except Exception as e:
            print(f"Error: {e}")

        print("\nAdvanced few-shot with schema:")
        try:
            advanced_result = advanced_few_shot_with_context(query, schema)
            blue_print(advanced_result)
        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "="*70 + "\n")

def demonstrate_pattern_learning():
    """Show how few-shot helps with specific formatting patterns"""

    print("=== PATTERN LEARNING DEMO ===\n")

    # Test different patterns
    patterns = {
        "Error Analysis": {
            "examples": [
                ("This query is slow", "ISSUE: Performance | CAUSE: Missing index | FIX: ADD INDEX idx_user_email ON users(email)"),
                ("Query returns wrong data", "ISSUE: Logic error | CAUSE: Incorrect JOIN condition | FIX: Change INNER JOIN to LEFT JOIN")
            ],
            "test": "Query times out"
        },
        "Code Review": {
            "examples": [
                ("SELECT * FROM users", "RATING: 2/5 | ISSUES: Using SELECT *, no WHERE clause | IMPROVE: Specify columns, add filtering"),
                ("SELECT u.id, u.name FROM users u WHERE u.active = 1", "RATING: 4/5 | ISSUES: None major | IMPROVE: Consider adding LIMIT for large datasets")
            ],
            "test": "SELECT COUNT(*) FROM orders o, users u WHERE o.user_id = u.id"
        }
    }

    for pattern_name, pattern_data in patterns.items():
        print(f"--- {pattern_name} Pattern ---")

        messages = [
            {"role": "system", "content": "You are a SQL expert. Follow the exact format shown in examples."}
        ]

        # Add examples
        for example_input, example_output in pattern_data["examples"]:
            messages.extend([
                {"role": "user", "content": example_input},
                {"role": "assistant", "content": example_output}
            ])

        # Add test query
        messages.append({"role": "user", "content": pattern_data["test"]})

        response = completion(
            model="openrouter/openai/gpt-oss-20b:free",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=messages,
            temperature=0.1
        )

        print(f"Input: {pattern_data['test']}")
        print("Output:")
        blue_print(response['choices'][0]['message']['content'])
        print()

if __name__ == "__main__":
    print("Few-Shot Learning Demo\n")

    # Main comparison
    compare_approaches()

    # Pattern learning demonstration
    demonstrate_pattern_learning()
