🚀 LangGraph Multi-Agent T-SQL to dbt Migration

🎯 Starting LangGraph migration workflow...

📊 TSQLAnalyst analyzing stored procedure...
🔄 DbtDeveloper creating dbt models...
⚡ DuckDBOptimizer optimizing for columnar analytics...

==================================================
📋 LANGGRAPH MIGRATION RESULTS
==================================================

✅ Migration completed successfully!

🔍 Final Agent: duckdb_optimizer

📊 Parsed Logic:
{
  "logic_components": [
    "Temporal aggregation using DATEADD/DATEDIFF functions",
    "SUM aggregation for monthly sales",
    "Window functions for ranking and rolling calculations"
  ],
  "data_sources": [
    "orders"
  ],
  "transformations": [
    "Monthly sales aggregation by customer",
    "Ranking customers by monthly sales",
    "3-month rolling sales calculation"
  ],
  "complex_patterns": {
    "has_cursor": false,
    "has_dynamic_sql": false,
    "has_temp_tables": true,
    "has_while_loops": false
  },
  "dependencies": [
    "orders table"
  ],
  "conversion_complexity": "medium"
}

🔄 Generated dbt Models:
{
  "staging_models": [
    {
      "name": "stg_orders",
      "sql": "SELECT * FROM {{ source('raw', 'orders') }} WHERE order_status = 'completed'",
      "materialization": "view"
    }
  ],
  "intermediate_models": [
    {
      "name": "int_monthly_sales",
      "sql": "SELECT date_trunc('month', order_date) as month_start, customer_id, SUM(order_total) as monthly_sales FROM {{ ref('stg_orders') }} GROUP BY 1, 2",
      "materialization": "table"
    }
  ],
  "mart_models": [
    {
      "name": "mart_sales_summary",
      "sql": "SELECT month_start, customer_id, monthly_sales, ROW_NUMBER() OVER (PARTITION BY month_start ORDER BY monthly_sales DESC) as rank, SUM(monthly_sales) OVER (PARTITION BY customer_id ORDER BY month_start ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_3month_sales FROM {{ ref('int_monthly_sales') }} WHERE monthly_sales > 0",
      "materialization": "table"
    }
  ],
  "tests": [
    "unique(mart_sales_summary, [month_start, customer_id])",
    "not_null(mart_sales_summary, [customer_id, monthly_sales])"
  ],
  "documentation": "Sales summary mart with customer ranking and rolling calculations"
}

⚡ DuckDB Optimizations:
{
  "columnar_optimizations": {
    "mart_sales_summary": [
      "month_start",
      "customer_id", 
      "monthly_sales",
      "rank",
      "rolling_3month_sales"
    ]
  },
  "function_conversions": [
    {
      "sql_server_function": "DATEADD(month, DATEDIFF(month, 0, order_date), 0)",
      "duckdb_function": "date_trunc('month', order_date)",
      "example": "date_trunc('month', '2024-01-15') = '2024-01-01'"
    }
  ],
  "memory_settings": {
    "max_memory": "4GB",
    "temp_directory": "/tmp/duckdb",
    "threads": 4
  },
  "performance_tips": [
    "Use parquet format for intermediate models",
    "Partition large fact tables by month",
    "Create indexes on frequently joined columns"
  ],
  "parquet_export": [
    "COPY mart_sales_summary TO 'output/sales_summary.parquet' (FORMAT PARQUET)"
  ]
}

🎯 LangGraph workflow completed with 0 errors