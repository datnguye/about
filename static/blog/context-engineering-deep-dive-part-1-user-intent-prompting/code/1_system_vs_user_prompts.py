"""
System vs User Prompts: Demonstrating proper separation of concerns

This script shows the difference between cramming everything into one message
vs properly separating system context from user requests.
"""

from os import getenv

from dotenv import load_dotenv
from litellm import completion

def blue_print(text):
    """Print text in blue color"""
    print(f"\033[94m{text}\033[0m")

# Load environment variables
load_dotenv()

def bad_approach():
    """Bad: Everything crammed into one message"""
    print("=== BAD APPROACH ===")

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[{
            "role": "user",
            "content": "You are a SQL expert. Fix this query: SELECT * FROM users WHERE age = '25'"
        }]
    )

    print("Query fix (bad approach):")
    blue_print(response["choices"][0]["message"]["content"])
    print("\n" + "="*50 + "\n")

def good_approach():
    """Good: Clear separation of concerns"""
    print("=== GOOD APPROACH ===")

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a SQL optimization expert. Focus on performance and security."
            },
            {
                "role": "user",
                "content": "Fix this query: SELECT * FROM users WHERE age = '25'"
            }
        ]
    )

    print("Query fix (good approach):")
    blue_print(response["choices"][0]["message"]["content"])

def compare_approaches():
    """Compare different system prompt strategies"""
    test_query = "SELECT * FROM orders o, users u WHERE o.user_id = u.id AND o.total > 1000"

    approaches = {
        "Generic": "You are a helpful assistant.",
        "Specific": "You are a SQL optimization expert with 10 years of experience.",
        "Context-Rich": """You are a senior database architect at a high-traffic e-commerce company.
        Your expertise includes query optimization, index design, and performance troubleshooting.
        Always consider scalability and maintainability in your recommendations."""
    }

    print("=== SYSTEM PROMPT COMPARISON ===")
    for approach_name, system_prompt in approaches.items():
        print(f"\n--- {approach_name} System Prompt ---")

        response = completion(
            model="openrouter/meta-llama/llama-3.1-8b-instruct",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Optimize this query: {test_query}"}
            ],
            temperature=0.3
        )

        blue_print(response["choices"][0]["message"]["content"])
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    print("System vs User Prompts Demo\n")

    # Demonstrate the difference
    bad_approach()
    good_approach()

    # Compare different system prompt strategies
    compare_approaches()
