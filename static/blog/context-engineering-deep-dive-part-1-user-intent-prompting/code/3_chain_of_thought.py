"""
Chain-of-Thought: Making the model show its reasoning

This script demonstrates how to get LLMs to think step-by-step,
providing transparency into their reasoning process.
"""

import json
from os import getenv

from dotenv import load_dotenv
from litellm import completion

def blue_print(text):
    """Print text in blue color"""
    print(f"\033[94m{text}\033[0m")

# Load environment variables
load_dotenv()

def analyze_query_performance(sql_query: str) -> dict:
    """Analyze SQL query with step-by-step reasoning"""

    cot_prompt = f"""
    Analyze this SQL query step by step:
    {sql_query}
    
    Follow these steps:
    1. Identify the tables involved
    2. Check for missing indexes
    3. Spot potential N+1 problems
    4. Suggest optimizations
    
    Show your reasoning for each step.
    """

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "You are a database performance expert. Think step-by-step."},
            {"role": "user", "content": cot_prompt}
        ],
        temperature=0.2  # Lower temperature for more focused reasoning
    )

    return {"analysis": response["choices"][0]["message"]["content"]}

def debug_slow_query(query: str, execution_stats: dict) -> dict:
    """Debug a slow query using chain-of-thought reasoning"""

    stats_text = json.dumps(execution_stats, indent=2)

    debug_prompt = f"""
    I have a slow SQL query that needs debugging. Let me walk through this systematically.
    
    Query:
    {query}
    
    Execution Statistics:
    {stats_text}
    
    Please debug this step by step:
    
    Step 1: Analyze the execution plan
    - What does the execution plan tell us?
    - Where are the bottlenecks?
    
    Step 2: Identify performance issues
    - What specific operations are slow?
    - Are there missing indexes?
    - Are there inefficient joins?
    
    Step 3: Propose solutions
    - What indexes should be added?
    - How can the query be rewritten?
    - What alternative approaches exist?
    
    Step 4: Estimate impact
    - How much improvement can we expect?
    - What are the trade-offs?
    
    Think through each step carefully and show your reasoning.
    """

    response = completion(
        model="openrouter/meta-llama/llama-3.1-70b-instruct",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a senior database performance engineer. Always show your step-by-step reasoning."
            },
            {"role": "user", "content": debug_prompt}
        ],
        temperature=0.3
    )

    return {"debug_analysis": response["choices"][0]["message"]["content"]}

def design_database_schema(requirements: str) -> dict:
    """Design database schema with explicit reasoning"""

    design_prompt = f"""
    Design a database schema for these requirements:
    {requirements}
    
    Work through this systematically:
    
    Step 1: Identify entities
    - What are the main objects/concepts?
    - What are their key attributes?
    
    Step 2: Define relationships
    - How do entities relate to each other?
    - What are the cardinalities (1:1, 1:N, N:N)?
    
    Step 3: Normalize the design
    - Are there any redundant data?
    - Should we split or merge tables?
    - What normal form should we target?
    
    Step 4: Consider performance
    - What queries will be most common?
    - Where should we add indexes?
    - Are there denormalization opportunities?
    
    Step 5: Plan for scale
    - How will this grow over time?
    - What are potential bottlenecks?
    
    Show your reasoning for each step and provide the final schema.
    """

    response = completion(
        model="openrouter/meta-llama/llama-3.1-70b-instruct",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a database architect. Always explain your design decisions step-by-step."
            },
            {"role": "user", "content": design_prompt}
        ],
        temperature=0.2
    )

    return {"schema_design": response["choices"][0]["message"]["content"]}

def compare_reasoning_approaches():
    """Compare direct vs chain-of-thought approaches"""

    test_query = """
    SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    WHERE u.created_at > '2024-01-01'
    GROUP BY u.id
    HAVING order_count > 5
    ORDER BY total_spent DESC
    """

    print("=== DIRECT vs CHAIN-OF-THOUGHT COMPARISON ===\n")

    # Direct approach
    print("--- Direct Approach ---")
    direct_response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "You are a SQL expert. Optimize this query."},
            {"role": "user", "content": f"Optimize this query: {test_query}"}
        ],
        temperature=0.3
    )
    blue_print(direct_response["choices"][0]["message"]["content"])

    print("\n" + "="*60 + "\n")

    # Chain-of-thought approach
    print("--- Chain-of-Thought Approach ---")
    cot_result = analyze_query_performance(test_query)
    blue_print(cot_result["analysis"])

def demonstrate_complex_reasoning():
    """Show chain-of-thought for complex database problems"""

    print("=== COMPLEX REASONING DEMO ===\n")

    # Example 1: Query debugging
    print("--- Query Debugging Example ---")
    slow_query = "SELECT * FROM orders o, users u, products p WHERE o.user_id = u.id AND o.product_id = p.id"
    execution_stats = {
        "execution_time": "15.2 seconds",
        "rows_examined": 50000000,
        "rows_returned": 25000,
        "temp_tables": 2,
        "filesort": True
    }

    debug_result = debug_slow_query(slow_query, execution_stats)
    blue_print(debug_result["debug_analysis"])

    print("\n" + "="*60 + "\n")

    # Example 2: Schema design
    print("--- Schema Design Example ---")
    requirements = """
    E-commerce platform requirements:
    - Users can place orders containing multiple products
    - Products belong to categories and have variants (size, color)
    - Track inventory levels for each product variant
    - Users have shipping addresses and payment methods
    - Need to handle returns and refunds
    - Support discount codes and promotions
    - Track user behavior and analytics
    """

    design_result = design_database_schema(requirements)
    blue_print(design_result["schema_design"])

if __name__ == "__main__":
    print("Chain-of-Thought Reasoning Demo\n")

    # Compare approaches
    compare_reasoning_approaches()

    print("\n" + "="*80 + "\n")

    # Complex reasoning examples
    demonstrate_complex_reasoning()
