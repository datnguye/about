"""
T-SQL to dbt Migration using LangGraph Multi-Agent Workflow
Demonstrates specialized agents working together using LangGraph orchestration.
"""

import json
from os import getenv
from typing import TypedDict

from dotenv import load_dotenv
from litellm import completion

try:
    from langgraph.graph import END, START, StateGraph
except ImportError:
    print("LangGraph not installed. Install with: uv add langgraph")
    StateGraph = None
    START = None
    END = None

load_dotenv()


class MigrationState(TypedDict):
    """State shared across migration agents"""

    tsql_procedure: str
    parsed_logic: dict
    dbt_models: dict
    optimizations: dict
    current_agent: str
    errors: list


def call_llm(messages: list, temperature: float = 0.2) -> str:
    """Helper function to call LLM with error handling"""
    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=messages,
        temperature=temperature,
    )

    content = response["choices"][0]["message"]["content"]

    # Handle markdown-wrapped JSON responses
    if content.strip().startswith("```json"):
        start = content.find("```json") + 7
        end = content.rfind("```")
        content = content[start:end].strip()
    elif content.strip().startswith("```"):
        start = content.find("```") + 3
        end = content.rfind("```")
        content = content[start:end].strip()

    return content


def tsql_analyst(state: MigrationState) -> MigrationState:
    """Expert in SQL Server internals, CTEs, cursors, and dynamic SQL"""

    print("📊 TSQLAnalyst analyzing stored procedure...")

    system_prompt = """You are a T-SQL expert specializing in stored procedure analysis.
    
    Analyze T-SQL procedures to extract:
    - Business logic and data transformations
    - Dependencies between objects
    - Complex patterns (cursors, dynamic SQL, temp tables)
    - Performance bottlenecks"""

    user_prompt = f"""
    Parse this T-SQL stored procedure:
    
    {state["tsql_procedure"]}
    
    Extract and return as JSON:
    {{
        "logic_components": ["list of business logic steps"],
        "data_sources": ["tables/views used"],
        "transformations": ["data transformation descriptions"],
        "complex_patterns": {{
            "has_cursor": true/false,
            "has_dynamic_sql": true/false,
            "has_temp_tables": true/false,
            "has_while_loops": true/false
        }},
        "dependencies": ["object dependencies"],
        "conversion_complexity": "low|medium|high"
    }}
    """

    try:
        content = call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        parsed_logic = json.loads(content)

        return {**state, "parsed_logic": parsed_logic, "current_agent": "tsql_analyst"}

    except (json.JSONDecodeError, ValueError) as e:
        return {
            **state,
            "parsed_logic": {},
            "current_agent": "tsql_analyst",
            "errors": [*state.get("errors", []), f"T-SQL analysis failed: {e!s}"],
        }


def dbt_developer(state: MigrationState) -> MigrationState:
    """Specializes in modern data transformation patterns and dbt best practices"""

    print("🔄 DbtDeveloper creating dbt models...")

    system_prompt = """You are a dbt expert specializing in converting T-SQL procedures to dbt models.
    
    Convert T-SQL logic to dbt models following:
    - Modular design (staging, intermediate, marts)
    - Incremental strategies where appropriate
    - Testing and documentation
    - Performance optimization"""

    user_prompt = f"""
    Generate dbt models from this parsed T-SQL logic:
    
    {json.dumps(state["parsed_logic"], indent=2)}
    
    Return dbt project structure as JSON:
    {{
        "staging_models": [
            {{
                "name": "stg_model_name",
                "sql": "SELECT statement",
                "materialization": "view"
            }}
        ],
        "intermediate_models": [
            {{
                "name": "int_model_name",
                "sql": "SELECT with transformations",
                "materialization": "table"
            }}
        ],
        "mart_models": [
            {{
                "name": "model_name",
                "sql": "Final SELECT",
                "materialization": "table|incremental",
                "unique_key": "column_name (if incremental)"
            }}
        ],
        "tests": ["suggested dbt tests"],
        "documentation": "model documentation"
    }}
    """

    try:
        content = call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
        )

        dbt_models = json.loads(content)

        return {**state, "dbt_models": dbt_models, "current_agent": "dbt_developer"}

    except (json.JSONDecodeError, ValueError) as e:
        return {
            **state,
            "dbt_models": {},
            "current_agent": "dbt_developer",
            "errors": [*state.get("errors", []), f"dbt generation failed: {e!s}"],
        }


def duckdb_optimizer(state: MigrationState) -> MigrationState:
    """Deep knowledge of columnar storage, parquet files, and in-memory processing"""

    print("⚡ DuckDBOptimizer optimizing for columnar analytics...")

    system_prompt = """You are a DuckDB expert specializing in performance optimization.
    
    Optimize dbt models for DuckDB:
    - Leverage columnar storage for analytics
    - Optimize parquet file output
    - Convert SQL Server functions to DuckDB
    - Configure memory settings
    - Add indexes and statistics"""

    user_prompt = f"""
    Optimize these dbt models for DuckDB:
    
    {json.dumps(state["dbt_models"], indent=2)}
    
    Return optimizations as JSON:
    {{
        "columnar_optimizations": {{
            "table_name": ["optimized column order for compression"]
        }},
        "function_conversions": [
            {{
                "sql_server_function": "DATEADD",
                "duckdb_function": "date_add or interval arithmetic",
                "example": "conversion example"
            }}
        ],
        "memory_settings": {{
            "max_memory": "4GB",
            "temp_directory": "/tmp/duckdb",
            "threads": 4
        }},
        "performance_tips": ["specific optimizations"],
        "parquet_export": ["COPY statements for parquet output"]
    }}
    """

    try:
        content = call_llm(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )

        optimizations = json.loads(content)

        return {
            **state,
            "optimizations": optimizations,
            "current_agent": "duckdb_optimizer",
        }

    except (json.JSONDecodeError, ValueError) as e:
        return {
            **state,
            "optimizations": {},
            "current_agent": "duckdb_optimizer",
            "errors": [*state.get("errors", []), f"DuckDB optimization failed: {e!s}"]
        }


def build_migration_workflow():
    """Build LangGraph workflow for T-SQL to dbt migration"""
    
    if StateGraph is None:
        raise ImportError("LangGraph not available. Install with: uv add langgraph")

    # Create the workflow graph
    workflow = StateGraph(MigrationState)

    # Add processing nodes
    workflow.add_node("analyze", tsql_analyst)
    workflow.add_node("convert", dbt_developer)
    workflow.add_node("optimize", duckdb_optimizer)

    # Define sequential flow
    workflow.add_edge(START, "analyze")
    workflow.add_edge("analyze", "convert")
    workflow.add_edge("convert", "optimize")
    workflow.add_edge("optimize", END)

    return workflow


def main():
    """Demonstrate LangGraph multi-agent T-SQL to dbt migration"""

    print("🚀 LangGraph Multi-Agent T-SQL to dbt Migration\n")

    # Sample T-SQL with complex patterns
    tsql_procedure = """
    CREATE PROCEDURE sp_sales_summary
    AS
    BEGIN
        -- Temp table for intermediate results
        SELECT
            DATEADD(month, DATEDIFF(month, 0, order_date), 0) as month_start,
            customer_id,
            SUM(order_total) as monthly_sales
        INTO #MonthlySales
        FROM orders
        WHERE order_status = 'completed'
        GROUP BY DATEADD(month, DATEDIFF(month, 0, order_date), 0), customer_id
        
        -- Complex aggregation with window functions
        SELECT
            month_start,
            customer_id,
            monthly_sales,
            ROW_NUMBER() OVER (PARTITION BY month_start ORDER BY monthly_sales DESC) as rank,
            SUM(monthly_sales) OVER (PARTITION BY customer_id ORDER BY month_start
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3month_sales
        FROM #MonthlySales
        WHERE monthly_sales > 0
    END
    """

    # Build and compile workflow
    workflow = build_migration_workflow()
    app = workflow.compile()

    # Execute migration workflow
    print("🎯 Starting LangGraph migration workflow...\n")

    initial_state = {
        "tsql_procedure": tsql_procedure,
        "parsed_logic": {},
        "dbt_models": {},
        "optimizations": {},
        "current_agent": "",
        "errors": [],
    }

    result = app.invoke(initial_state)

    # Display results
    print("\n" + "=" * 50)
    print("📋 LANGGRAPH MIGRATION RESULTS")
    print("=" * 50)

    if result.get("errors"):
        print("❌ Errors encountered:")
        for error in result["errors"]:
            print(f"   • {error}")
    else:
        print("✅ Migration completed successfully!")

    print(f"\n🔍 Final Agent: {result['current_agent']}")

    print("\n📊 Parsed Logic:")
    print(json.dumps(result["parsed_logic"], indent=2))

    print("\n🔄 Generated dbt Models:")
    print(json.dumps(result["dbt_models"], indent=2))

    print("\n⚡ DuckDB Optimizations:")
    print(json.dumps(result["optimizations"], indent=2))

    print(
        f"\n🎯 LangGraph workflow completed with {len(result.get('errors', []))} errors"
    )


if __name__ == "__main__":
    main()
