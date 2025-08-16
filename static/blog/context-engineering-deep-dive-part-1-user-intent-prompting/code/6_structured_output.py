"""
Structured Output: Force reliable JSON responses from LLMs

This script demonstrates techniques to get consistently formatted,
parseable outputs instead of messy text responses.
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


def extract_structured_data(text: str, schema: dict) -> dict:
    """Extract structured data with guaranteed format"""

    format_prompt = f"""
    Extract information and return ONLY valid JSON matching this schema:

    Schema: {json.dumps(schema, indent=2)}

    Text: {text}

    Rules:
    - Return ONLY the JSON object, no explanation
    - Use null for missing values
    - Validate types match the schema
    """

    response = completion(
        model="openrouter/openai/gpt-oss-20b",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a JSON extraction expert. Output only valid JSON.",
            },
            {"role": "user", "content": format_prompt},
        ],
        temperature=0,  # Zero temperature for deterministic output
    )

    return json.loads(response["choices"][0]["message"]["content"])


def create_json_enforcer(output_schema: dict, max_retries: int = 3):
    """Create a function that enforces JSON output with retries"""

    def enforce_json_output(prompt: str, system_message: str | None = None) -> dict:
        """Enforce JSON output with automatic retries on parse failures"""

        json_prompt = f"""
        {prompt}

        CRITICAL: Return ONLY valid JSON matching this exact schema:
        {json.dumps(output_schema, indent=2)}

        Rules:
        - NO explanatory text
        - NO markdown formatting
        - NO code blocks
        - ONLY the JSON object
        - ALL required fields must be present
        """

        system_msg = (
            system_message or "You are a JSON-only API. Return only valid JSON."
        )

        for attempt in range(max_retries):
            try:
                response = completion(
                    model="openrouter/openai/gpt-oss-20b",
                    api_key=getenv("OPENROUTER_API_KEY"),
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": json_prompt},
                    ],
                    temperature=0.1,
                )

                result_text = response["choices"][0]["message"]["content"].strip()

                # Try to clean common formatting issues
                if result_text.startswith("```json"):
                    result_text = (
                        result_text.replace("```json", "").replace("```", "").strip()
                    )
                elif result_text.startswith("```"):
                    result_text = result_text.replace("```", "").strip()

                # Parse and validate
                parsed = json.loads(result_text)

                # Basic schema validation
                if validate_schema(parsed, output_schema):
                    return parsed
                else:
                    raise ValueError("Schema validation failed")

            except (json.JSONDecodeError, ValueError) as e:
                if attempt == max_retries - 1:
                    raise Exception(
                        f"Failed to get valid JSON after {max_retries} attempts: {e}"
                    ) from e

                # Add more explicit instructions for retry
                json_prompt += f"\n\nATTEMPT {attempt + 2}: Previous attempt failed. Return ONLY valid JSON."

        return None

    return enforce_json_output


def validate_schema(data: dict, schema: dict) -> bool:
    """Basic schema validation"""

    if not isinstance(data, dict):
        return False

    # Check required keys exist
    return all(key in data for key in schema)


def demonstrate_query_analysis():
    """Demonstrate structured query analysis"""

    analysis_schema = {
        "tables": ["list of table names"],
        "operations": ["list of SQL operations"],
        "complexity": "low|medium|high",
        "estimated_runtime": "seconds as integer",
        "potential_issues": ["list of potential problems"],
        "optimization_suggestions": ["list of improvements"],
        "confidence_score": "float between 0 and 1",
    }

    enforcer = create_json_enforcer(analysis_schema)

    queries_to_analyze = [
        """
        SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.created_at > '2024-01-01'
        GROUP BY u.id
        HAVING order_count > 5
        ORDER BY total_spent DESC
        """,
        """
        SELECT * FROM products p, categories c, orders o, order_items oi
        WHERE p.category_id = c.id
        AND oi.product_id = p.id
        AND oi.order_id = o.id
        """,
        """
        SELECT user_id FROM sessions WHERE last_activity > NOW() - INTERVAL 1 HOUR
        """,
    ]

    print("=== STRUCTURED QUERY ANALYSIS ===\n")

    for i, query in enumerate(queries_to_analyze, 1):
        print(f"--- Analysis {i} ---")
        print(f"Query: {query.strip()}")

        try:
            result = enforcer(
                f"Analyze this SQL query and provide structured output: {query}",
                "You are a SQL analysis API that returns only JSON.",
            )

            print("Analysis:")
            blue_print(json.dumps(result, indent=2))
            print()

        except Exception as e:
            print(f"Error: {e}")
            print()


def demonstrate_security_audit():
    """Demonstrate structured security audit output"""

    security_schema = {
        "vulnerability_level": "low|medium|high|critical",
        "vulnerabilities_found": ["list of security issues"],
        "sql_injection_risk": "boolean",
        "data_exposure_risk": "boolean",
        "recommendations": ["list of security fixes"],
        "compliant_with_standards": ["list of standards: OWASP, PCI-DSS, etc"],
        "audit_score": "integer 1-10",
    }

    security_enforcer = create_json_enforcer(security_schema)

    vulnerable_queries = [
        "SELECT * FROM users WHERE username = '" + "user_input" + "'",
        "SELECT * FROM credit_cards WHERE user_id = 123",
        "SELECT password_hash, salt FROM users WHERE email = ?",
        "UPDATE users SET admin = 1 WHERE user_id = " + "user_controlled_id",
    ]

    print("=== STRUCTURED SECURITY AUDIT ===\n")

    for i, query in enumerate(vulnerable_queries, 1):
        print(f"--- Security Audit {i} ---")
        print(f"Query: {query}")

        try:
            result = security_enforcer(
                f"Perform a security audit on this SQL query: {query}",
                "You are a security audit API that identifies vulnerabilities and returns only JSON.",
            )

            print("Security Audit:")
            blue_print(json.dumps(result, indent=2))
            print()

        except Exception as e:
            print(f"Error: {e}")
            print()


def demonstrate_performance_report():
    """Demonstrate structured performance reporting"""

    performance_schema = {
        "estimated_execution_time": "string with units",
        "resource_usage": {
            "cpu_intensive": "boolean",
            "memory_intensive": "boolean",
            "io_intensive": "boolean",
        },
        "scalability_concerns": ["list of scalability issues"],
        "recommended_indexes": ["list of index suggestions"],
        "alternative_approaches": ["list of alternative query strategies"],
        "bottlenecks": ["list of performance bottlenecks"],
        "optimization_priority": "low|medium|high",
    }

    perf_enforcer = create_json_enforcer(performance_schema)

    performance_queries = [
        """
        SELECT COUNT(*) FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.created_at > '2023-01-01'
        """,
        """
        SELECT u.*,
               (SELECT COUNT(*) FROM orders WHERE user_id = u.id) as order_count,
               (SELECT SUM(total) FROM orders WHERE user_id = u.id) as total_spent
        FROM users u
        """,
        """
        SELECT * FROM logs
        WHERE message LIKE '%error%'
        AND created_at BETWEEN '2024-01-01' AND '2024-12-31'
        ORDER BY created_at DESC
        """,
    ]

    print("=== STRUCTURED PERFORMANCE REPORT ===\n")

    for i, query in enumerate(performance_queries, 1):
        print(f"--- Performance Report {i} ---")
        print(f"Query: {query.strip()}")

        try:
            result = perf_enforcer(
                f"Analyze the performance characteristics of this query: {query}",
                "You are a database performance analysis API that returns only JSON.",
            )

            print("Performance Report:")
            blue_print(json.dumps(result, indent=2))
            print()

        except Exception as e:
            print(f"Error: {e}")
            print()


def test_edge_cases():
    """Test edge cases and error handling"""

    simple_schema = {
        "status": "success|error",
        "message": "string",
        "data": "any valid JSON value or null",
    }

    edge_enforcer = create_json_enforcer(simple_schema)

    edge_cases = [
        "Analyze this completely invalid SQL: SELECT * FROM nowhere WHERE nothing = everything",
        "What is the meaning of life?",
        "Generate a SQL query for something impossible",
        "",  # Empty input
    ]

    print("=== EDGE CASES TEST ===\n")

    for i, edge_case in enumerate(edge_cases, 1):
        print(f"--- Edge Case {i} ---")
        print(f"Input: '{edge_case}'")

        try:
            result = edge_enforcer(
                edge_case, "Handle any input and return structured JSON response."
            )

            print("Response:")
            blue_print(json.dumps(result, indent=2))
            print()

        except Exception as e:
            print(f"Error: {e}")
            print()


if __name__ == "__main__":
    print("Structured Output Demo\n")

    # Basic structured data extraction
    schema = {
        "tables": ["list of table names"],
        "operations": ["list of SQL operations"],
        "complexity": "low|medium|high",
        "estimated_runtime": "seconds as integer",
    }

    query_text = "This query joins users with orders and filters by date, grouping results by region"
    print("=== BASIC EXTRACTION ===")
    print(f"Input: {query_text}")
    try:
        result = extract_structured_data(query_text, schema)
        print("Extracted:")
        blue_print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 80 + "\n")

    # Comprehensive demonstrations
    demonstrate_query_analysis()

    print("=" * 80 + "\n")

    demonstrate_security_audit()

    print("=" * 80 + "\n")

    demonstrate_performance_report()

    print("=" * 80 + "\n")

    test_edge_cases()
