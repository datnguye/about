"""
Example 1: Function Calling Evolution
Demonstrates the evolution from JSON parsing to native function calling
"""

import json
from litellm import completion
from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()


def old_way_json_parsing():
    """The old way: Begging the LLM to output valid JSON"""
    print("=== Old Way: JSON Parsing ===\n")

    prompt = """
    Analyze this SQL query and return EXACTLY this format:
    {
      "action": "optimize_query",
      "query": "SELECT * FROM users WHERE age > 25",
      "suggestions": ["Add index on age column", "Use specific columns instead of *"]
    }
    IMPORTANT: Output ONLY valid JSON, nothing else!
    """

    response = completion(
        model="openrouter/openai/gpt-4o-mini",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[{"role": "user", "content": prompt}],
    )

    # Try to parse the response
    response_text = response.choices[0].message.content
    print(f"Raw response:\n{response_text}\n")

    try:
        action = json.loads(response_text)
        print("✅ Successfully parsed JSON:")
        print(json.dumps(action, indent=2))
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print("Would need regex fallback here...")


def modern_way_function_calling():
    """Modern way: Native function calling"""
    print("\n=== Modern Way: Function Calling ===\n")

    # Define function schema
    tools = [
        {
            "type": "function",
            "function": {
                "name": "optimize_query",
                "description": "Optimize a SQL query for performance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to optimize",
                        },
                        "target_db": {
                            "type": "string",
                            "enum": ["postgres", "mysql", "snowflake"],
                            "description": "Target database system",
                        },
                        "suggestions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of optimization suggestions",
                        },
                    },
                    "required": ["query", "suggestions"],
                },
            },
        }
    ]

    response = completion(
        model="openrouter/openai/gpt-4o-mini",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "user",
                "content": "Optimize this query: SELECT * FROM users WHERE age > 25",
            }
        ],
        tools=tools,
        tool_choice="auto",
    )

    # Clean, structured, guaranteed format
    if response.choices[0].message.get("tool_calls"):
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"✅ Function called: {tool_call.function.name}")
        print("Arguments received:")

        # Parse the arguments
        args = json.loads(tool_call.function.arguments)
        print(json.dumps(args, indent=2))

        # Now you can safely use the structured data
        print(f"\nQuery to optimize: {args['query']}")
        print(f"Target DB: {args.get('target_db', 'Not specified')}")
        print("Suggestions:")
        for i, suggestion in enumerate(args["suggestions"], 1):
            print(f"  {i}. {suggestion}")
    else:
        print("No function call made")


if __name__ == "__main__":
    print("Function Calling Evolution Demo\n")
    print("=" * 50)

    # Show both approaches
    old_way_json_parsing()
    modern_way_function_calling()