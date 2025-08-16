+++
title = "User Intent & Prompting: Making LLMs understand what you really want"
description = "Ever tried explaining something to someone and they completely misunderstood you? Now imagine that someone is an AI that takes everything literally. Let's master the art of prompt engineering and intent recognition."
date = 2025-01-16
template = "blog_page.html"

[extra]
author = "Dat Nguyen"
tags = ["LLM", "PromptEngineering", "NLP", "AI", "UserIntent", "ContextEngineering"]
read_time = "8 min read"
featured_image = "/blog/context-engineering-deep-dive-part-1-user-intent-prompting/hero.png"
toc = true
toc_depth = 1
show_ads = true
enable_auto_related = true
+++
![Visualization of prompt engineering concepts showing the translation of user intent into structured LLM instructions with arrows connecting human language to machine understanding](/blog/context-engineering-deep-dive-part-1-user-intent-prompting/hero.png)

First thing first:

{% quote() %}
LLMs don't remember you.<br>They don't learn from your preferences.<br>They don't grow with you.
{% end %}

Every conversation starts from zero. That brilliant solution you worked out together yesterday? Gone. Your coding style preferences? Never existed. It's like having a colleague with no memory who reads the same Wikipedia snapshot from 2023 every morning.

This is the gap every AI project tries to bridge. The spoiler?

They're all running on something called ⭐ **Workflow** ⭐ — structured chains of steps that actually work. We'll get to that more clearly in the whole deep dive series, starting with "Prompting" in this article.

## The Problem: Translation Lost

Ever tried explaining something to someone and they completely misunderstood you? Now imagine that someone is an AI that takes everything literally. That's prompting in a nutshell.

You ask ChatGPT to "improve" your code, and it rewrites the entire thing in a completely different style. You tell Claude to be "concise" and it gives you one-word answers. When you ask an LLM to "make it better", what exactly does "better" mean? More concise? More detailed? More formal?

In this deep dive, we're tackling the foundation of every LLM interaction: getting these models to actually understand what you want.

{% tip(type="note", title="About the Code Examples") %}
All the code examples in this article use [LiteLLM](https://docs.litellm.ai/) for unified API calls and [OpenRouter](https://openrouter.ai/) for accessing various models (including free ones). This keeps the examples practical and reproducible without requiring expensive API keys.

All is backed with [uv](https://docs.astral.sh/uv/) — a python package manager. Go check the [README](/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/README.md) file if you'd like to run scripts by yourself, remember to get your `OPENROUTER_API_KEY` in advance!
{% end %}

## 1. **The Intent Gap: What You Think vs What You Say**

Here's a fun experiment. Ask any LLM to "analyze this data" without providing context. Watch it struggle. Now ask a colleague the same thing — they'll immediately ask "what kind of analysis?" or "what are you looking for?". That's the intent gap right there.

### Real Examples of Prompt Failures

The classic one? "Make this function better":

```python
def calculate(x, y):
    return x * y + 10 + 10
```

- 👨‍🦱 What you meant: "_**Optimize for performance**_"
- 🤖 What the LLM heard: "_**Rewrite everything with type hints, docstrings, and error handling**_"

The LLM might give you a _50-line class with [dependency injection](https://fastapi.tiangolo.com/tutorial/dependencies/)_ when all you wanted was a faster multiplication algorithm.

**Why Context Matters more than You Think**:

LLMs are like contractors showing up to a job site with no blueprints. Sure, they have all the tools, but without context, they're just guessing what you want built.

**The Hidden Assumptions in Your Requests**:

When you say "summarize this", you're assuming the model knows:
- How long the summary should be
- Who the audience is
- What details matter most
- Whether to preserve technical accuracy or prioritize clarity

Spoiler: It doesn't know any of that.

Instead, it makes its best guess — which often means hallucinating details or asking clarifying questions when you're using a reasoning model.

## 2. **Prompt Engineering Fundamentals**

Let's cut through the fluff. Here are the patterns that actually work.

### System vs User Prompts: Who Does What?

Think of system prompts as the LLM's job description. User prompts are the specific tasks. Mix them up, and you get a confused AI trying to be helpful in all the wrong ways.

```python
from litellm import completion
from dotenv import load_dotenv
from os import getenv

# Load environment variables
load_dotenv()

# Bad: Everything crammed into one message
response = completion(
    model="openrouter/openai/gpt-oss-20b:free",
    api_key=getenv("OPENROUTER_API_KEY"),
    messages=[{
        "role": "user",
        "content": "You are a SQL expert. Fix this query: SELECT * FROM users WHERE age = '25'"
    }]
)

# Good: Clear separation of concerns
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
print(response["choices"][0]["message"]["content"])
# Output: "SELECT * FROM users WHERE age = 25 -- Fixed: removed quotes from numeric comparison"
```

{{ code_example(
  script="1_system_vs_user_prompts.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/1_system_vs_user_prompts.py",
  command="uv run 1_system_vs_user_prompts.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/1_system_vs_user_prompts.md"
) }}


### The Power of Few-Shot Learning

Want the LLM to follow a specific pattern? Show it examples. It's like training a new developer — show them how it's done, not just what to do.

```python
def extract_sql_from_text(user_query: str) -> str:
    """Extract SQL from natural language using few-shot examples"""

    response = completion(
        model="openrouter/openai/gpt-oss-20b:free",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "Extract SQL queries from natural language. Return only valid SQL."},
            # Few-shot examples
            {"role": "user", "content": "Show me all users from Texas"},
            {"role": "assistant", "content": "SELECT * FROM users WHERE state = 'TX';"},
            {"role": "user", "content": "Count orders from last month"},
            {
                "role": "assistant",
                "content": "SELECT COUNT(*) FROM orders WHERE date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH);"
            },
            # Actual query
            {"role": "user", "content": user_query}
        ]
    )

    return response["choices"][0]["message"]["content"]

# Now it knows the pattern
print(extract_sql_from_text("Find customers who spent over 1000"))
# Output: "SELECT * FROM customers WHERE total_spent > 1000;"
```

{{ code_example(
  script="2_few_shot_learning.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/2_few_shot_learning.py",
  command="uv run 2_few_shot_learning.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/2_few_shot_learning.md"
) }}

### Chain-of-Thought: Making the Model Show Its Work

Sometimes you need the LLM to think step-by-step. It's like debugging — you want to see the logic, not just the answer.

```python
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
        model="openrouter/meta-llama/llama-3.1-70b-instruct",  # Bigger model for complex reasoning
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a database performance expert. Think step-by-step."
            },
            {"role": "user", "content": cot_prompt}
        ],
        temperature=0.2  # Lower temperature for more focused reasoning
    )

    return {"analysis": response["choices"][0]["message"]["content"]}

# Example usage
complex_query = """
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
HAVING order_count > 5
"""

result = analyze_query_performance(complex_query)
# Returns detailed step-by-step analysis with reasoning
```

{{ code_example(
  script="3_chain_of_thought.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/3_chain_of_thought.py",
  command="uv run 3_chain_of_thought.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/3_chain_of_thought.md"
) }}


{% tip(
    type="info", 
    title="Want more Prompt Engineering examples?"
) %}
For a comprehensive collection of prompting techniques and examples, check out the [Prompt Engineering Guide](https://www.promptingguide.ai/). It's an excellent resource that covers everything from basic prompts to advanced techniques like tree-of-thought reasoning.
{% end %}

## 3. **Advanced Prompting Patterns**

Now for the tricks that separate amateur hour from production-ready systems.

### Role-Playing Prompts: More Than Just "You Are A..."

The difference between "You are a SQL expert" and a proper role definition? About 10x in output quality.

```python
def create_expert_analyzer(expertise_level: str = "senior"):
    """Create specialized SQL analyzer with detailed role definition"""

    roles = {
        "junior": "You are a junior developer learning SQL best practices.",
        "senior": ("You are a senior database architect with 15 years "
                  "optimizing Fortune 500 databases."),
        "security": ("You are a database security specialist focused on "
                    "SQL injection prevention.")
    }

    def analyze(query: str, context: str = "") -> str:
        system_prompt = f"""
        {roles.get(expertise_level, roles['senior'])}

        Your approach:
        - Identify issues before suggesting fixes
        - Explain trade-offs, not just solutions
        - Consider the business context
        - Provide actionable recommendations

        Response format:
        1. ISSUES FOUND: [list]
        2. IMPACT: [business impact]
        3. RECOMMENDATIONS: [specific fixes]
        4. ALTERNATIVE APPROACHES: [if applicable]
        """

        response = completion(
            model="openrouter/anthropic/claude-3.5-sonnet",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nQuery: {query}"}
            ],
            temperature=0.3
        )

        return response["choices"][0]["message"]["content"]

    return analyze

# Usage
security_analyzer = create_expert_analyzer("security")
result = security_analyzer(
    "SELECT * FROM users WHERE username = '" + user_input + "'",
    context="Public-facing login system"
)
# Returns detailed security analysis with SQL injection warnings
```

{{ code_example(
  script="4_role_playing_prompts.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/4_role_playing_prompts.py",
  command="uv run 4_role_playing_prompts.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/4_role_playing_prompts.md"
) }}

### Constraint-Based Prompting: Setting Boundaries That Work

Want consistent outputs? Don't ask nicely. Set hard constraints.

```python
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
    """

    prompt = f"""
    Generate a migration script for these changes:
    {json.dumps(changes, indent=2)}

    {constraints}

    Output format: Valid SQL with comments
    """

    response = completion(
        model="openrouter/meta-llama/llama-3.1-70b-instruct",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {"role": "system", "content": "You are a database migration expert. Safety is paramount."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1  # Low temperature for consistency
    )

    return response["choices"][0]["message"]["content"]
```

{{ code_example(
  script="5_constraint_based_prompting.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/5_constraint_based_prompting.py",
  command="uv run 5_constraint_based_prompting.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/5_constraint_based_prompting.md"
) }}

### Output Formatting: Force Structure from the Start

Stop parsing messy LLM outputs. Force structured responses from the beginning.

```python
import json

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
        model="openrouter/anthropic/claude-3.5-sonnet",
        api_key=getenv("OPENROUTER_API_KEY"),
        messages=[
            {
                "role": "system",
                "content": "You are a JSON extraction expert. Output only valid JSON."
            },
            {"role": "user", "content": format_prompt}
        ],
        temperature=0  # Zero temperature for deterministic output
    )

    return json.loads(response["choices"][0]["message"]["content"])

# Example usage
schema = {
    "tables": ["list of table names"],
    "operations": ["list of SQL operations"],
    "complexity": "low|medium|high",
    "estimated_runtime": "seconds as integer"
}

query_text = "This query joins users with orders and filters by date"
result = extract_structured_data(query_text, schema)
# Output: {"tables": ["users", "orders"], "operations": ["JOIN", "WHERE"], ...}
```

{{ code_example(
  script="6_structured_output.py",
  script_url="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/6_structured_output.py",
  command="uv run 6_structured_output.py",
  output="/blog/context-engineering-deep-dive-part-1-user-intent-prompting/code/llm_response/6_structured_output.md"
) }}

## Key Takeaways

- **Context beats cleverness** — A clear system prompt with specific constraints outperforms fancy prompting tricks every time
- **Examples > explanations** — Few-shot learning with 2-3 examples teaches patterns better than long descriptions
- **Structure first, content second** — Force JSON outputs and defined formats to avoid parsing nightmares
- **Temperature matters** — Use 0-0.2 for consistent outputs, 0.3-0.7 for creative tasks
- **Chain-of-thought when it counts** — For complex reasoning, make the model show its work
- **Role definition depth** — "Senior DBA with 15 years experience" gets better results than "SQL expert"

## What's Next?

Ready to dive deeper? Let's explore how agents use these prompts to actually reason and make decisions...

---

*Technical deep dive series — Part 1 of 5*

**[← Back to Overview](/blog/internal/context-engineering-modern-llm-ecosystem/)** | **[Part 2: Agents & Reasoning →](/blog/internal/upcoming/)**
<!-- **[← Back to Overview](/blog/internal/context-engineering-modern-llm-ecosystem/)** | **[Part 2: Agents & Reasoning →](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)** -->

