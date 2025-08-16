"""
Constraint-Based Prompting: Setting hard boundaries for consistent outputs

This script demonstrates how to use strict constraints and rules
to get reliable, predictable outputs from LLMs.
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


def generate_migration_script(changes: dict) -> str:
    """Generate database migration with strict constraints"""

    constraints = """
    HARD CONSTRAINTS (MUST follow):
    - Use transactions for all DDL operations
    - Include rollback statements
    - Add IF EXISTS checks
    - Maximum 5 operations per transaction
    - Include timing estimates as comments

    FORBIDDEN:
    - Direct table drops without backups
    - Changing primary keys
    - Removing columns without deprecation notice
    - Operations without explicit transaction boundaries

    REQUIRED FORMAT:
    - Start with migration metadata comment
    - Each operation in separate transaction
    - Rollback script at the end
    """

    prompt = f"""
    Generate a migration script for these changes:
    {json.dumps(changes, indent=2)}

    {constraints}

    Output format: Valid SQL with comments
    """

    response = completion(
        model="openrouter/openai/gpt-oss-20b",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a database migration expert. Safety is paramount.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,  # Low temperature for consistency
    )

    return response["choices"][0]["message"]["content"]


def create_constrained_query_generator(rules: dict):
    """Create a query generator with specific business rules"""

    def generate_query(request: str, context: dict | None = None) -> str:
        constraints_text = "MANDATORY CONSTRAINTS:\n"
        for category, rule_list in rules.items():
            constraints_text += f"\n{category.upper()}:\n"
            for rule in rule_list:
                constraints_text += f"  - {rule}\n"

        context_text = ""
        if context:
            context_text = f"\nCONTEXT:\n{json.dumps(context, indent=2)}\n"

        prompt = f"""
        Generate SQL query for: {request}

        {constraints_text}
        {context_text}

        VIOLATION OF ANY CONSTRAINT WILL RESULT IN REJECTION.

        Return only valid SQL that follows ALL constraints.
        """

        response = completion(
            model="openrouter/openai/gpt-oss-20b",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a SQL generator. You MUST follow all constraints exactly. Never violate security or performance rules.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,  # Zero temperature for maximum consistency
        )

        return response["choices"][0]["message"]["content"]

    return generate_query


def create_security_constrained_generator():
    """Generator with strict security constraints"""

    security_rules = {
        "security": [
            "NEVER use dynamic SQL construction",
            "ALWAYS use parameterized queries",
            "NO direct string concatenation in WHERE clauses",
            "MUST validate all input parameters",
            "Include SQL injection prevention comments",
        ],
        "performance": [
            "ALWAYS include LIMIT clauses for potentially large result sets",
            "USE specific column names, never SELECT *",
            "Include index hints when beneficial",
            "AVOID N+1 query patterns",
        ],
        "compliance": [
            "LOG all data access attempts",
            "MASK sensitive data in output",
            "INCLUDE audit trail information",
            "RESPECT data retention policies",
        ],
    }

    return create_constrained_query_generator(security_rules)


def create_performance_constrained_generator():
    """Generator focused on performance constraints"""

    performance_rules = {
        "optimization": [
            "ALWAYS use appropriate indexes",
            "LIMIT result sets to maximum 1000 rows",
            "USE covering indexes when possible",
            "AVOID subqueries in SELECT lists",
            "PREFER JOINs over EXISTS when possible",
        ],
        "resource_management": [
            "NO queries estimated to run > 30 seconds",
            "MAXIMUM 3 table joins without special approval",
            "USE read replicas for reporting queries",
            "INCLUDE query execution plan comments",
        ],
        "monitoring": [
            "ADD query tags for monitoring",
            "INCLUDE estimated row count comments",
            "SPECIFY timeout hints",
            "LOG slow query warnings",
        ],
    }

    return create_constrained_query_generator(performance_rules)


def validate_constraint_adherence():
    """Test how well the model follows constraints"""

    print("=== CONSTRAINT ADHERENCE TEST ===\n")

    # Test migration generation
    print("--- Migration Script Generation ---")
    migration_changes = {
        "add_table": "user_preferences",
        "add_columns": ["theme", "notification_settings"],
        "add_index": "idx_user_preferences_user_id",
    }

    migration_script = generate_migration_script(migration_changes)
    print("Generated Migration:")
    blue_print(migration_script)
    print("-" * 50)

    # Test security constraints
    print("\n--- Security Constrained Generator ---")
    security_gen = create_security_constrained_generator()

    security_requests = [
        "Find users by email address",
        "Get user login history",
        "Search products by name",
    ]

    for request in security_requests:
        print(f"\nRequest: {request}")
        try:
            result = security_gen(request, {"max_results": 100, "user_role": "admin"})
            print("Generated Query:")
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")

    print("-" * 50)

    # Test performance constraints
    print("\n--- Performance Constrained Generator ---")
    perf_gen = create_performance_constrained_generator()

    perf_requests = [
        "Get top selling products",
        "Find customers with high order values",
        "Generate monthly sales report",
    ]

    for request in perf_requests:
        print(f"\nRequest: {request}")
        try:
            result = perf_gen(request, {"reporting_period": "last_30_days"})
            print("Generated Query:")
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")


def demonstrate_constraint_enforcement():
    """Show how constraints prevent unwanted outputs"""

    print("=== CONSTRAINT ENFORCEMENT DEMO ===\n")

    # Create a generator with strict output format constraints
    format_rules = {
        "output_format": [
            "MUST return valid JSON only",
            "NO explanatory text outside JSON",
            "INCLUDE confidence score (0-1)",
            "REQUIRED fields: query, explanation, estimated_cost",
            "USE lowercase keys only",
        ],
        "query_rules": [
            "MAXIMUM 100 characters per line",
            "PROPER indentation (2 spaces)",
            "INCLUDE query type comment",
            "END with semicolon",
        ],
    }

    print("Testing format constraints:")
    requests = [
        "Count active users",
        "Find expensive orders",
        "List product categories",
    ]

    for request in requests:
        print(f"\nRequest: {request}")
        try:
            # Override the generator to force JSON format
            constraints_text = "MANDATORY CONSTRAINTS:\n"
            for category, rule_list in format_rules.items():
                constraints_text += f"\n{category.upper()}:\n"
                for rule in rule_list:
                    constraints_text += f"  - {rule}\n"

            prompt = f"""
            Generate SQL query for: {request}

            {constraints_text}

            RETURN ONLY VALID JSON:
            {{
                "query": "SQL query here",
                "explanation": "brief explanation",
                "estimated_cost": "low|medium|high",
                "confidence": 0.95
            }}

            NO OTHER TEXT ALLOWED.
            """

            response = completion(
                model="openrouter/openai/gpt-oss-20b",
                api_key=getenv("OPENROUTER_API_KEY"),
                messages=[
                    {
                        "role": "system",
                        "content": "You are a JSON-only SQL generator. Output ONLY valid JSON. No explanations.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
            )

            result = response["choices"][0]["message"]["content"]
            print("JSON Output:")
            blue_print(result)

            # Try to parse as JSON to validate
            try:
                json.loads(result)
                print("✓ Valid JSON format")
            except json.JSONDecodeError:
                print("✗ Invalid JSON format")

        except Exception as e:
            print(f"Error: {e}")


def test_boundary_conditions():
    """Test edge cases and constraint violations"""

    print("=== BOUNDARY CONDITIONS TEST ===\n")

    # Test what happens when constraints conflict
    conflicting_rules = {
        "performance": ["MUST use indexes", "NO table scans allowed"],
        "flexibility": ["MUST handle any query type", "SUPPORT ad-hoc queries"],
        "security": ["MUST validate everything", "NO dynamic SQL"],
        "speed": ["MUST return results in <1 second", "OPTIMIZE for speed"],
    }

    conflict_gen = create_constrained_query_generator(conflicting_rules)

    difficult_requests = [
        "Search all text fields for any mention of a user-provided term",
        "Generate a dynamic report with user-defined columns and filters",
        "Find similar records using fuzzy matching across all tables",
    ]

    for request in difficult_requests:
        print(f"Challenging request: {request}")
        try:
            result = conflict_gen(request)
            print("Response:")
            blue_print(result)
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 40)


if __name__ == "__main__":
    print("Constraint-Based Prompting Demo\n")

    # Test basic constraint adherence
    validate_constraint_adherence()

    print("\n" + "=" * 80 + "\n")

    # Demonstrate format enforcement
    demonstrate_constraint_enforcement()

    print("\n" + "=" * 80 + "\n")

    # Test edge cases
    test_boundary_conditions()
