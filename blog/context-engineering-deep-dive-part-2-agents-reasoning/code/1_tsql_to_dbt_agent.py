"""
T-SQL to dbt Migration Agent
Demonstrates how an agent reasons through stored procedure conversion using multi-step analysis.
"""

import json
from os import getenv
from typing import Any

from dotenv import load_dotenv
from litellm import completion

load_dotenv()


class TSQLToDbtAgent:
    """Agent that converts T-SQL stored procedures to dbt models"""

    def __init__(self):
        self.api_key = getenv("OPENROUTER_API_KEY")
        self.model = "openrouter/openai/gpt-oss-20b:free"

    def analyze_tsql_procedure(self, tsql_code: str) -> dict[str, Any]:
        """Parse and understand T-SQL stored procedure logic"""

        system_prompt = """You are a T-SQL expert specializing in stored procedure analysis.

        Analyze the given stored procedure and identify:
        1. Main components (CTEs, temp tables, cursors, dynamic SQL)
        2. Data transformations and business logic
        3. Dependencies and data flow
        4. Complexity factors that affect migration

        Think step-by-step through the procedure logic."""

        user_prompt = f"""
        Analyze this T-SQL stored procedure:

        {tsql_code}

        Return analysis as JSON:
        {{
            "procedure_name": "name",
            "components": {{
                "ctes": ["list of CTEs"],
                "temp_tables": ["list of temp tables"],
                "cursors": ["cursor details"],
                "updates": ["update statements"],
                "dynamic_sql": true/false
            }},
            "business_logic": "description of what the procedure does",
            "data_flow": ["step-by-step data flow"],
            "complexity": "simple|moderate|complex",
            "migration_challenges": ["specific challenges for dbt conversion"]
        }}
        """

        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        try:
            content = response["choices"][0]["message"]["content"]
            # Handle markdown-wrapped JSON responses
            if content.strip().startswith("```json"):
                content = content.strip()
                start = content.find("```json") + 7
                end = content.rfind("```")
                content = content[start:end].strip()
            elif content.strip().startswith("```"):
                content = content.strip()
                start = content.find("```") + 3
                end = content.rfind("```")
                content = content[start:end].strip()
            
            return json.loads(content)
        except (json.JSONDecodeError, ValueError) as e:
            return {
                "error": f"Failed to parse analysis: {str(e)}",
                "raw": response["choices"][0]["message"]["content"],
            }

    def convert_to_dbt(self, tsql_analysis: dict[str, Any]) -> dict[str, Any]:
        """Convert analyzed T-SQL to dbt models"""

        system_prompt = """You are a dbt expert specializing in converting T-SQL procedures to dbt models.

        Your approach:
        - Convert procedural logic to declarative SQL
        - Replace temp tables with CTEs or staging models
        - Convert cursors to window functions or incremental models
        - Optimize for DuckDB's columnar architecture
        - Follow dbt best practices (modularity, testing, documentation)"""

        user_prompt = f"""
        Convert this analyzed T-SQL procedure to dbt:

        Analysis: {json.dumps(tsql_analysis, indent=2)}

        Generate dbt model structure as JSON:
        {{
            "models": [
                {{
                    "name": "model_name",
                    "type": "staging|intermediate|mart",
                    "materialization": "view|table|incremental",
                    "sql": "SELECT statement",
                    "tests": ["suggested tests"],
                    "documentation": "model description"
                }}
            ],
            "conversion_notes": ["important conversion decisions"],
            "duckdb_optimizations": ["columnar storage, parquet output, memory settings"],
            "validation_queries": ["queries to validate data matches original"]
        }}
        """

        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        try:
            return json.loads(response["choices"][0]["message"]["content"])
        except json.JSONDecodeError:
            return {
                "error": "Failed to generate dbt models",
                "raw": response["choices"][0]["message"]["content"],
            }

    def validate_conversion(
        self, original_tsql: str, dbt_models: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate that dbt models preserve the original logic"""

        system_prompt = """You are a data validation expert. Compare T-SQL procedures with dbt models
        to ensure logic preservation and identify any discrepancies.

        Focus on:
        - Business logic accuracy
        - Data transformation equivalence
        - Edge case handling
        - Performance implications"""

        user_prompt = f"""
        Validate this conversion:

        ORIGINAL T-SQL:
        {original_tsql}

        DBT MODELS:
        {json.dumps(dbt_models, indent=2)}

        Return validation report as JSON:
        {{
            "logic_preserved": true/false,
            "confidence_score": 0.0-1.0,
            "matched_transformations": ["list of correctly converted logic"],
            "discrepancies": ["list of potential issues"],
            "missing_logic": ["logic not captured in dbt"],
            "recommendations": ["improvement suggestions"],
            "test_scenarios": ["suggested test cases"]
        }}
        """

        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        try:
            return json.loads(response["choices"][0]["message"]["content"])
        except json.JSONDecodeError:
            return {
                "error": "Failed to validate",
                "raw": response["choices"][0]["message"]["content"],
            }


def main():
    """Demonstrate T-SQL to dbt migration agent"""

    print("🚀 T-SQL to dbt Migration Agent Demo\n")

    # Sample T-SQL stored procedure
    tsql_procedure = """
    CREATE PROCEDURE sp_customer_sales_analysis
    AS
    BEGIN
        -- Create temp table for customer aggregates
        CREATE TABLE #CustomerMetrics (
            customer_id INT,
            total_sales DECIMAL(10,2),
            order_count INT,
            last_order_date DATE
        )

        -- Populate with CTEs
        ;WITH CustomerOrders AS (
            SELECT
                customer_id,
                SUM(order_total) as total_sales,
                COUNT(*) as order_count,
                MAX(order_date) as last_order_date
            FROM orders
            WHERE order_status = 'completed'
            GROUP BY customer_id
        ),
        CustomerSegments AS (
            SELECT
                customer_id,
                CASE
                    WHEN total_sales > 10000 THEN 'VIP'
                    WHEN total_sales > 5000 THEN 'Premium'
                    ELSE 'Standard'
                END as segment
            FROM CustomerOrders
        )
        INSERT INTO #CustomerMetrics
        SELECT * FROM CustomerOrders;

        -- Update with cursor for complex logic
        DECLARE @customer_id INT
        DECLARE customer_cursor CURSOR FOR
            SELECTcustomer_id FROM #CustomerMetrics
            WHERE total_sales > 1000

        OPEN customer_cursor
        FETCH NEXT FROM customer_cursor INTO @customer_id

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Complex business logic here
            UPDATE #CustomerMetrics
            SET total_sales = total_sales * 1.1
            WHERE customer_id = @customer_id

            FETCH NEXT FROM customer_cursor INTO @customer_id
        END

        CLOSE customer_cursor
        DEALLOCATE customer_cursor

        -- Return results
        SELECT * FROM #CustomerMetrics
    END
    """

    # Initialize agent
    agent = TSQLToDbtAgent()

    # Step 1: Analyze T-SQL
    print("📊 Step 1: Analyzing T-SQL procedure...")
    analysis = agent.analyze_tsql_procedure(tsql_procedure)
    print(json.dumps(analysis, indent=2))

    # Step 2: Convert to dbt
    print("\n🔄 Step 2: Converting to dbt models...")
    dbt_models = agent.convert_to_dbt(analysis)
    print(json.dumps(dbt_models, indent=2))

    # Step 3: Validate conversion
    print("\n✅ Step 3: Validating conversion...")
    validation = agent.validate_conversion(tsql_procedure, dbt_models)
    print(json.dumps(validation, indent=2))

    print("\n🎯 Migration Complete!")
    print(f"Confidence Score: {validation.get('confidence_score', 0):.1%}")


if __name__ == "__main__":
    main()
