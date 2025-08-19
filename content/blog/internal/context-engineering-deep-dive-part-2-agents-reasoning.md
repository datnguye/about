+++
title = "Agents & Reasoning: When LLMs Learn to Think Before They Speak"
description = "Single LLM calls are like having one genius locked in a room. Agents? They're like having an entire team with specialized skills, memory, and tools. The difference?"
date = 2025-08-17
template = "blog_page.html"

[extra]
authors = [
  { name = "Dat Nguyen", title = "Data & AI @ Tech Lead", github = "datnguye", linkedin = "datnguye" }
]
tags = ["AI-Agents", "ReasoningEngine", "LangGraph", "CrewAI", "MultiAgent", "LLM"]
read_time = "9 min read"
featured_image = "/blog/context-engineering-deep-dive-part-2-agents-reasoning/hero.png"
toc = true
toc_depth = 1
show_ads = true
enable_auto_related = true
+++

![Agents & Reasoning: When LLMs Learn to Think Before They Speak](/blog/context-engineering-deep-dive-part-2-agents-reasoning/hero.png)

Your LLM can write code, answer questions, and generate content. But can it plan a complex project, break it down, delegate tasks, and coordinate results? That's where agents come in — and things get REALLY interesting.

## The Reality Check

Single LLM calls are like having one genius locked in a room. Agents? They're like having an entire team with specialized skills, memory, and the ability to use tools.

Remember how we talked about [prompt engineering and user intent](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/) in Part 1? That's your foundation. But when problems get complex — like analyzing a dataset, writing code, debugging it, and then generating a report — you need something more powerful.

Here's the thing: **Agent** vs **Workflow**, they are essentially the same. Someone renamed the 'workflow' and became rich. Therefore, we will use 'agent' wording from now on.

## From Chatbots to Agents: The Evolution

Traditional LLMs are reactive. You ask, they answer. Done. But real work is never that simple.

Take migrating from T-SQL stored procedures to DuckDB dbt. You need to:
1. Parse complex T-SQL logic with CTEs, temp tables, and cursors
2. Convert procedural code to dbt's declarative SQL models  
3. Transform SQL Server functions to DuckDB equivalents
4. Restructure dependencies into dbt's DAG pattern
5. Validate output data matches the original procedures

Each step depends on the previous one's results. That's where agents come in — they can loop back, self-correct, and adapt their approach based on what they discover.

**The reasoning gap** is real. Ask GPT-4 to "convert this stored procedure to dbt," and you'll get a generic SELECT statement. Ask an agent? It'll first parse your T-SQL logic, identify cursor patterns that need window functions, map SQL Server functions to DuckDB equivalents, create modular staging and mart models, and validate the outputs match.

**Where agents absolutely crush it for database migrations:**
- Parsing complex stored procedures with nested logic and dependencies
- Converting procedural patterns (cursors, loops) to set-based SQL  
- Mapping hundreds of SQL Server functions to DuckDB equivalents
- Iteratively validating that migrated models produce identical results

## Agent Architecture Patterns (Single Agent)

### ReAct: Reasoning + Acting

The [ReAct](https://www.promptingguide.ai/techniques/react) pattern is beautifully simple. Instead of thinking OR acting, your agent alternates between reasoning about what to do next and actually doing it:

1. Reasoning (`thought`) - The agent thinks about what to do next
2. Acting (`action`) - The agent takes a concrete action
3. Observing (`observation`) - The agent sees the results and uses them for the next reasoning step

```python
# ReAct loop for T-SQL to dbt conversion
def convert_stored_procedure(tsql_proc):
    # INITIAL REASONING
    thought = llm.think(f"Analyzing T-SQL procedure: {tsql_proc.name}")
    # Agent thinks: "This proc has 3 CTEs, 2 temp tables, and a cursor - needs staging models"

    # INITIAL ACTION  
    action = parse_tsql_structure(tsql_proc)
    observation = {"ctes": 3, "temp_tables": 2, "cursors": 1}

    # ITERATIVE LOOP
    while not conversion_complete(observation):
        # REASONING: What should I do next based on what I observed?
        thought = llm.think(f"Given {observation}, what's the next conversion step?")
        # "Convert cursor to window functions, temp tables to CTEs"

        # ACTING: Take the action identified in reasoning
        action = convert_next_component(thought)
        observation = execute_conversion(action)
        # "Successfully converted cursor to ROW_NUMBER() OVER()"
    
    return generate_dbt_model(observation)
```

### Plan-and-Execute

The Plan-and-Execute pattern, formalized in the research ([Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)), separates strategic planning from tactical execution. This two-phase approach excels when tasks have complex dependencies or require resource coordination.

T-SQL procedures with dependencies need upfront planning. The agent creates a migration roadmap, identifies dependencies, then executes systematically.

```python
# Planning T-SQL to dbt migration strategy
def plan_migration_strategy(tsql_database):
    # Step 1: Analyze all stored procedures and dependencies
    migration_plan = llm.create_migration_plan(tsql_database)
    # Plan: "Convert base tables first, then staging procs, then reporting procs"
    
    # Step 2: Execute migration in dependency order
    migrated_models = []
    for proc in migration_plan.ordered_procedures:
        result = migrate_procedure(proc, dependencies=migrated_models)
        migrated_models.append(result)
        
        # Adapt plan if complex logic discovered
        if result.has_dynamic_sql or result.has_nested_cursors:
            migration_plan = llm.revise_plan(migration_plan, result)
            # "Found dynamic SQL - need intermediate Python model"
    
    return create_dbt_project(migrated_models)
```

### Self-Reflection

Or [Reflexion](https://www.promptingguide.ai/techniques/reflexion), enables iterative improvement through self-critique. Unlike traditional one-shot generation, reflective agents evaluate their own outputs, identify flaws, and refine their approach across multiple iterations.

Agents that critique their own dbt models. They generate, validate against original T-SQL, and iterate until the logic matches perfectly.

```python
# Self-reflection for dbt model validation
def validate_dbt_conversion(tsql_proc, initial_dbt_model):
    current_model = initial_dbt_model
    
    while True:
        # Compare outputs between T-SQL and dbt
        validation = llm.compare_outputs(tsql_proc, current_model)
        
        if validation.data_match_percentage > 99.5:
            break  # Near-perfect match achieved
            
        # Identify specific logic mismatches
        issues = validation.find_logic_differences()
        # "DATEADD function converted incorrectly"
        # "GROUP BY rollup not preserved"
        
        # Self-correct the dbt model
        current_model = llm.fix_dbt_model(current_model, issues)
    
    return current_model
```

{{ code_example(
  script="1_tsql_to_dbt_agent.py",
  script_url="/blog/context-engineering-deep-dive-part-2-agents-reasoning/code/1_tsql_to_dbt_agent.py",
  command="uv run 1_tsql_to_dbt_agent.py",
  output="/blog/context-engineering-deep-dive-part-2-agents-reasoning/code/llm_response/1_tsql_to_dbt_agent.md"
) }}

## Multi-Agent Systems (MAS)

[MAS](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) means that multiple **specialized agents** working together can handle complex migrations which would overwhelm a single agent. Think of it like a migration team — T-SQL experts, dbt developers, DuckDB optimizers, and validators working in concert.

Many popular frameworks like [**LangGraph**](https://github.com/langchain-ai/langgraph) orchestrate these migrations. Each agent brings specialized expertise:

```python
# LangGraph team for T-SQL to dbt migration
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MigrationState(TypedDict):
    tsql_procedure: str
    parsed_logic: dict
    dbt_models: dict
    optimizations: dict
    current_agent: str
    
def tsql_analyst(state: MigrationState) -> MigrationState:
    """Expert in SQL Server internals, CTEs, cursors, and dynamic SQL"""
    parsed_logic = analyze_tsql_structure(state["tsql_procedure"])
    return {**state, "parsed_logic": parsed_logic, "current_agent": "analyst"}

def dbt_developer(state: MigrationState) -> MigrationState:
    """Specializes in modern data transformation patterns and dbt best practices"""
    dbt_models = convert_to_dbt_models(state["parsed_logic"])
    return {**state, "dbt_models": dbt_models, "current_agent": "developer"}

def duckdb_optimizer(state: MigrationState) -> MigrationState:
    """Deep knowledge of columnar storage, parquet files, and in-memory processing"""
    optimizations = optimize_for_duckdb(state["dbt_models"])
    return {**state, "optimizations": optimizations, "current_agent": "optimizer"}

# Build migration workflow
workflow = StateGraph(MigrationState)
workflow.add_node("analyze", tsql_analyst)
workflow.add_node("convert", dbt_developer)
workflow.add_node("optimize", duckdb_optimizer)

# Define sequential flow
workflow.add_edge(START, "analyze")
workflow.add_edge("analyze", "convert")
workflow.add_edge("convert", "optimize")
workflow.add_edge("optimize", END)

# Execute migration
app = workflow.compile()
result = app.invoke({
    "tsql_procedure": "CREATE PROCEDURE sp_customer_analytics AS ...",
    "parsed_logic": {},
    "dbt_models": {},
    "optimizations": {},
    "current_agent": ""
})
```

{{ code_example(
  script="2_multi_agent_workflow.py",
  script_url="/blog/context-engineering-deep-dive-part-2-agents-reasoning/code/2_multi_agent_workflow.py",
  command="uv run 2_multi_agent_workflow.py",
  output="/blog/context-engineering-deep-dive-part-2-agents-reasoning/code/llm_response/2_multi_agent_workflow.md"
) }}

The agents collaborate by passing parsed logic, suggesting optimizations, and validating each other's work.

Looking great? Yes indeed, but be careful with pitfalls! The key to effective isn't throwing more agents at the problem — it's finding the sweet spot between parallelization and coordination overhead. Stick to a good number of specialized agents, run independent tasks in parallel while keeping dependent workflows sequential, batch similar procedures through the same agent to reduce context switching, cache common patterns between agents, and use early exit conditions when confidence thresholds are met.

Too many agents will create chaos, while too few miss opportunities.

## Key Takeaways

- **Agents ≠ Workflows**: They're the same concept rebranded — structured sequences that can loop back, self-correct, and adapt based on observations
- **Architecture patterns unlock complexity**: ReAct for iterative analysis, Plan-and-Execute for dependency management, Self-Reflection for validation loops
- **Multi-agent sweet spot**: 3-5 specialized agents with clear boundaries beat large teams — focus on parallelizing independent tasks while keeping dependencies sequential

## Next Up

Now that our agents can think and reason, how do they access the knowledge they need? Enter RAG systems...

---

*Technical deep dive series — Part 2 of 5*

**[← Part 1: User Intent & Prompting](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)** | **[Part 3: RAG Systems →](/blog/upcoming/)**

📚 **Context Engineering Deep Dive Series:**

1. [User Intent & Prompting: The Art of Making LLMs Understand What You Really Want](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)
2. **Agents & Reasoning** (You are here)
3. [RAG Systems: When Your LLM Needs to Phone a Friend](/blog/internal/context-engineering-deep-dive-part-3-rag-systems/)
4. [Action Tools: How LLMs Finally Learned to Stop Talking and Start Doing](/blog/internal/upcoming/)
5. [Memory Systems: Teaching LLMs to Remember (Without Going Broke)](/blog/upcoming/)

🎯 **Start with the overview:** [Context Engineering: How RAG, agents, and memory make LLMs actually useful](/blog/internal/context-engineering-modern-llm-ecosystem/)