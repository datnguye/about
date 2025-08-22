+++
title = "Action Tools: How LLMs Finally Learned to Stop Talking and Start Doing"
description = "An LLM that can only generate text is like a brilliant consultant who can't touch a keyboard. Function calling changed everything — now your AI can actually ship code, query databases, and send emails."
date = 2025-08-21
template = "blog_page.html"

[extra]
authors = [
  { name = "Dat Nguyen", title = "Data & AI @ Tech Lead", github = "datnguye", linkedin = "datnguye" }
]
tags = ["LLM", "FunctionCalling", "Tools", "LangChain", "MCP", "ContextEngineering"]
read_time = "10 min read"
featured_image = "/blog/context-engineering-deep-dive-part-4-action-tools/hero.png"
toc = true
toc_depth = 1
show_ads = true
enable_auto_related = true
+++

![Visualization showing LLM function calling architecture with tools branching out from a central AI model to various APIs and services](/blog/context-engineering-deep-dive-part-4-action-tools/hero.png)

An LLM without tools is just an expensive autocomplete.

Give it function calling, and suddenly it's writing code, running queries, and sending emails.

**The power?** Immense. **The risks?** Let's talk about those too.

Remember when we had to parse LLM outputs with regex to trigger actions? Dark times! I'm happy for you if you don't even know this story, the later doesn't always be worse. Now, models can directly call functions, use tools, and interact with the real world, subsequently create massive implication.

## 1. **From Text to Action: The Evolution**

Let's cut through the fluff. Before function calling, we were stuck in the dark ages of "parse and pray." We'd beg the LLM to output valid JSON:

```python
# The old way: Begging the LLM to output valid JSON
prompt = """
Analyze this SQL query and return EXACTLY this format:
{
  "action": "optimize_query",
  "query": "...",
  "suggestions": [...]
}
IMPORTANT: Output ONLY valid JSON, nothing else PLEASE, I'm begging you, bruh!
"""

response = llm.complete(prompt)
# Pray it's valid JSON
try:
    action = json.loads(response)  # 50% chance of failure
except:
    # Welcome to regex hell
    action = extract_json_with_regex(response)
```

June 2023 changed everything. OpenAI introduced function calling, and suddenly we had structured, reliable tool use:

```python
from litellm import completion
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Modern way: Define your function schema
tools = [{
    "type": "function",
    "function": {
        "name": "optimize_query",
        "description": "Optimize a SQL query for performance",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query to optimize"},
                "target_db": {"type": "string", "enum": ["postgres", "mysql", "snowflake"]}
            },
            "required": ["query"]
        }
    }
}]

response = completion(
    model="openrouter/openai/gpt-oss-20b:free",
    api_key=getenv("OPENROUTER_API_KEY"),
    messages=[{"role": "user", "content": "Optimize: SELECT * FROM users WHERE age > 25"}],
    tools=tools,
    tool_choice="auto"
)

# Clean, structured, guaranteed format
if response.choices[0].message.get("tool_calls"):
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Function: {tool_call.function.name}")
    print(f"Arguments: {tool_call.function.arguments}")
```

{{ code_example(
  script="1_function_calling_evolution.py",
  script_url="/blog/context-engineering-deep-dive-part-4-action-tools/code/1_function_calling_evolution.py",
  command="uv run 1_function_calling_evolution.py",
  output="/blog/context-engineering-deep-dive-part-4-action-tools/code/llm_response/1_function_calling_evolution.md"
) }}

Here's what nobody explains clearly about the terminology: [**Function Calling**](https://platform.openai.com/docs/guides/function-calling) (OpenAI's approach), [**Tool Use**](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) (Anthropic's terminology), and **Actions** (what everyone else calls it) — they're all the same thing. The model decides which function to call and with what parameters. No more regex, no more prayer. Just clean, structured execution.

## 2. **Building Safe Tool Interfaces**

Now that we understand how function calling evolved from regex hell to structured tool use, let's tackle the critical question: how do we build tools that won't accidentally destroy our production systems?

Want to give an LLM database access? Here's how to not destroy everything:

### The Pydantic Approach: Type Safety First

```python
from typing import Literal
from pydantic import BaseModel, Field, field_validator
import re

class DatabaseQuery(BaseModel):
    """Tool for read-only database queries with multiple safety layers"""
    
    query: str = Field(description="SQL query to execute")
    database: Literal["staging", "analytics"] = Field(
        default="staging",
        description="Target database (prod not available)"
    )
    timeout_seconds: int = Field(default=30, le=60, description="Query timeout")
    
    @field_validator("query")
    def validate_query(cls, v):
        """Multi-layer query validation"""
        # Layer 1: No destructive operations
        dangerous_keywords = ["DELETE", "UPDATE", "DROP", "ALTER", "TRUNCATE", "INSERT"]
        query_upper = v.upper()
        
        for keyword in dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', query_upper):
                raise ValueError(f"Destructive operation '{keyword}' not allowed")
        
        # Layer 2: Must be a SELECT query
        if not query_upper.strip().startswith("SELECT"):
            raise ValueError("Only SELECT queries allowed")
        
        # Layer 3: Limit check
        if "LIMIT" not in query_upper:
            v = f"{v.rstrip(';')} LIMIT 1000"  # Force limit
        
        return v
    
    def execute(self):
        """Execute with additional runtime checks"""
        # Connection would use read-only credentials
        # Wrapped in timeout context
        # Full audit logging
        pass
```

{{ code_example(
  script="2_safe_tool_interfaces.py",
  script_url="/blog/context-engineering-deep-dive-part-4-action-tools/code/2_safe_tool_interfaces.py",
  command="uv run 2_safe_tool_interfaces.py",
  output="/blog/context-engineering-deep-dive-part-4-action-tools/code/llm_response/2_safe_tool_interfaces.md"
) }}

### The Defense-in-Depth Pattern

Never trust a single validation layer:

```python
from functools import wraps
import time
from typing import Any, Callable

def rate_limit(calls_per_minute: int = 10):
    """Rate limiting decorator"""
    def decorator(func: Callable) -> Callable:
        call_times = []
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            now = time.time()
            # Clean old calls
            call_times[:] = [t for t in call_times if now - t < 60]
            
            if len(call_times) >= calls_per_minute:
                raise Exception(f"Rate limit exceeded: {calls_per_minute}/min")
            
            call_times.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def audit_log(func: Callable) -> Callable:
    """Audit logging decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            # Log success
            print(f"✅ {func.__name__} succeeded in {time.time() - start_time:.2f}s")
            return result
        except Exception as e:
            # Log failure
            print(f"❌ {func.__name__} failed: {str(e)}")
            raise
    return wrapper

@audit_log
@rate_limit(calls_per_minute=5)
def execute_tool(tool_name: str, params: dict) -> Any:
    """Execute tool with all safety layers"""
    # Validation, execution, monitoring
    pass
```

## 3. **Tool Categories That Matter**

With our safety patterns in place — type validation, rate limiting, and defense-in-depth — we need to understand which tools we're actually building. Because let's be honest: giving an LLM the ability to send emails is very different from letting it read documentation.

Not all tools are created equal. Here's the hierarchy of danger:

### 🟢 Safe Tools (Start Here)

```python
# Read-only operations
safe_tools = {
    "search_documentation": "Read API docs",
    "query_analytics": "Read-only database queries",
    "fetch_metrics": "Get performance data",
    "list_files": "Directory listings"
}
```

### 🟡 Moderate Risk Tools (Add Safeguards)

```python
# State changes with limits
moderate_tools = {
    "send_slack_message": "Rate limited, specific channels only",
    "create_jira_ticket": "Template-based, no custom fields",
    "generate_report": "Resource limits, sandboxed execution",
    "cache_invalidation": "Specific keys only"
}
```

### 🔴 High Risk Tools (Human Approval Required)

```python
# Never fully automated
dangerous_tools = {
    "execute_code": "Arbitrary code execution",
    "database_write": "Data modifications",
    "send_email": "External communications",
    "deploy_code": "Production changes"
}
```

{{ code_example(
  script="3_tool_categories.py",
  script_url="/blog/context-engineering-deep-dive-part-4-action-tools/code/3_tool_categories.py",
  command="uv run 3_tool_categories.py",
  output="/blog/context-engineering-deep-dive-part-4-action-tools/code/llm_response/3_tool_categories.md"
) }}

## 4. **The LangChain Toolkit Approach**

Understanding tool risk categories is crucial, but managing individual tools manually gets overwhelming fast. This is where orchestration frameworks shine — and LangChain has become the de facto standard.

LangChain makes tool orchestration almost too easy. Here's production-ready patterns:

### Building a SQL Toolkit

```python
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from litellm import completion
from langchain_community.llms.base import LLM
from typing import Any, List, Optional

class LiteLLMWrapper(LLM):
    """Wrapper to use LiteLLM with LangChain"""
    model: str = "openrouter/openai/gpt-oss-20b:free"
    api_key: str
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        response = completion(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "user", "content": prompt}],
            stop=stop
        )
        return response.choices[0].message.content
    
    @property
    def _llm_type(self) -> str:
        return "litellm"

# Safe database connection
db = SQLDatabase.from_uri(
    "sqlite:///example.db",  # Use read-only connection in production
    sample_rows_in_table_info=3
)

# Create agent with safety features
llm = LiteLLMWrapper(api_key=getenv("OPENROUTER_API_KEY"))

agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",  # Use tool calling
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,  # Prevent infinite loops
    max_execution_time=30  # Timeout protection
)

# Safe execution with error handling
try:
    result = agent.invoke({
        "input": "What are the top 5 customers by revenue?"
    })
except Exception as e:
    print(f"Execution failed safely: {e}")
```

{{ code_example(
  script="4_langchain_toolkit.py",
  script_url="/blog/context-engineering-deep-dive-part-4-action-tools/code/4_langchain_toolkit.py",
  command="uv run 4_langchain_toolkit.py",
  output="/blog/context-engineering-deep-dive-part-4-action-tools/code/llm_response/4_langchain_toolkit.md"
) }}

### Custom Tool Creation

```python
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel

class CodeAnalysisInput(BaseModel):
    file_path: str
    analysis_type: Literal["security", "performance", "style"]

def analyze_code(file_path: str, analysis_type: str) -> str:
    """Analyze code with specific focus"""
    # Implementation here
    return f"Analysis of {file_path} for {analysis_type}"

# Structured tool with schema
code_analyzer = StructuredTool.from_function(
    func=analyze_code,
    name="code_analyzer",
    description="Analyze code for security, performance, or style issues",
    args_schema=CodeAnalysisInput,
    return_direct=False,  # Let agent process results
    handle_tool_error=True  # Graceful error handling
)
```

## 5. **All-in-One with MCP (Model Context Protocol)**

We've seen how to build tools with LangChain, categorize them by risk, and implement safety patterns. But managing all these integrations across different LLM providers gets complex fast. Enter MCP — Anthropic's answer to the tool integration chaos.

Anthropic's [MCP](https://www.anthropic.com/news/model-context-protocol) is the new kid on the block — and it's quickly becoming the standard everyone's adopting. Instead of rehashing the theory (plenty of that out there already), let's dive straight into a real implementation.

I'll use the official [time server](https://github.com/modelcontextprotocol/servers/tree/main/src/time) as a practical example — a real MCP server that demonstrates STDIO communication (for others or to implement a custom one, see [here](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) for more details):

### MCP Configuration

The beauty of MCP is its configuration-based approach. Just like Claude Desktop or VS Code, you define which servers to use:

```bash
uv add mcp-server-time      # Install Time serber
uv add mcp                  # Install MCP Python SDK
```

Here's how to build an LLM agent using MCP - just like configuring Claude Desktop:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from litellm import completion

class MCPAgent:
    """LLM Agent with MCP server configuration"""
    
    def __init__(self, mcp_config):
        """Configure like Claude Desktop:
        mcp_config = {
            "time": {"command": "uvx", "args": ["mcp-server-time"]}
        }
        """
        self.mcp_config = mcp_config
        self.available_tools = []

    async def setup(self):
        """Discover tools from MCP servers"""
        for server_name, config in self.mcp_config.items():
            try:
                # Start MCP server and get tools
                command = [config["command"]] + config["args"]
                session, cleanup_ctx = await self.create_session(command)
                
                tools = await session.list_tools()
                self.available_tools.extend([
                    {"name": t.name, "description": t.description} 
                    for t in tools.tools
                ])
                
                print(f"✅ {server_name}: {len(tools.tools)} tools available")
                await self.cleanup_session(cleanup_ctx)
                
            except Exception as e:
                print(f"❌ {server_name}: {e}")

    async def chat(self, message: str):
        """Chat with LLM using MCP tools"""
        response = completion(
            model="openrouter/openai/gpt-4o-mini",
            api_key=getenv("OPENROUTER_API_KEY"),
            messages=[{"role": "user", "content": message}],
            tools=self.format_tools_for_llm(),
            tool_choice="auto"
        )
        
        # Execute any tool calls through MCP
        if response.choices[0].message.tool_calls:
            await self.execute_tools(response.choices[0].message.tool_calls)
        
        return response.choices[0].message.content

# Simple usage
async def main():
    agent = MCPAgent({
        "time": {"command": "uvx", "args": ["mcp-server-time"]}
    })
    
    await agent.setup()
    result = await agent.chat("What time is it in Tokyo?")
    print(result)

asyncio.run(main())
```

{{ code_example(
  script="5_mcp_example.py",
  script_url="/blog/context-engineering-deep-dive-part-4-action-tools/code/5_mcp_example.py",
  command="uv run 5_mcp_example.py",
  output="/blog/context-engineering-deep-dive-part-4-action-tools/code/llm_response/5_mcp_example.md"
) }}

{% tip(type="info", title="dbt MCP Server") %}
Want to see MCP in action with data analysis coupling with dbt? Check out the official server:
- **[dbt-mcp](https://github.com/modelcontextprotocol/servers/tree/main/src/dbt)** - Query dbt models and metrics

All available via `uvx <server-name>`
{% end %}

{% tip(type="note", title="Why MCP Matters") %}
MCP standardizes how LLMs interact with external tools. Instead of building custom integrations for each LLM provider, you build one MCP server and it works everywhere. Think of it as the USB-C of AI tools.
{% end %}

## The Risk: Nobody wants to mention

We've covered the technical implementation — from function calling to MCP servers. But here's where theory meets reality, and where most teams learn expensive lessons.

Give an LLM database write access? Email sending capabilities? Code execution? Each tool is a potential footgun. Here's how to not shoot yourself:

**Production Checklist**

What actually works in production? Here are the non-negotiable rules:

1. **Least Privilege**: Read-only by default, always
2. **Validate Everything**: Never trust LLM-generated parameters
3. **Audit Everything**: If it's not logged, it didn't happen
4. **Circuit Breakers**: Automatic shutoff for suspicious patterns
5. **Human in the Loop**: Critical operations need approval
6. **Sandbox Execution**: Isolate tool execution environment
7. **Cost Controls**: Set spending limits per tool
8. **Rollback Ready**: Every action must be reversible

Every tool configuration needs these safety requirements:
- Rate limiting (reasonable limits, not 1000 calls per minute)
- Timeout controls
- Audit logging enabled
- Sandbox mode for execution
- Clear rollback strategy

And remember: tools that can modify data (write to databases, send emails, delete files) MUST have audit logging enabled. No exceptions.

**Some potential honour stories**:

1. **The $72K OpenAI Bill**: No rate limiting on a code generation tool. LLM went into a loop.
2. **The Dropped Production Table**: `DROP TABLE` wasn't in the blocklist. Guess what happened.
3. **The Email Storm**: LLM sent 10,000 emails before anyone noticed. No rate limiting.
4. **The Infinite Loop**: Tool called itself recursively. No iteration limits.

## Key Takeaways

- **Start with read-only tools** — You can always add write capabilities later, but you can't undo a dropped table
- **Defense in depth is not optional** — Input validation + rate limiting + audit logs + circuit breakers + human approval for critical ops
- **MCP is now the standard** — Standardized tool interfaces mean write once, use everywhere (when it's mature)

## What's Next?

Your agents can think (reasoning), access knowledge (RAG), and take actions (tools). But what about remembering what happened 5 minutes ago? Or last week? Time to dive into memory systems...

---

*Technical deep dive series — Part 4 of 5*

**[← Part 3: RAG Systems](/blog/internal/context-engineering-deep-dive-part-3-rag-systems/)** | **[Part 5: Memory Systems →](/blog/internal/context-engineering-deep-dive-part-5-memory-systems/)**

## Related Articles in This Series

📚 **Context Engineering Deep Dive Series:**

1. [User Intent & Prompting: Making LLMs understand what you really want](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)
2. [Agents & Reasoning: When LLMs Learn to Think Before They Speak](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)
3. [RAG Systems: When Your LLM Needs to Phone a Friend](/blog/internal/context-engineering-deep-dive-part-3-rag-systems/)
4. **Action Tools** (You are here)
5. [Memory Systems: Teaching LLMs to Remember (Without Going Broke)](/blog/internal/context-engineering-deep-dive-part-5-memory-systems/)

🎯 **Start with the overview:** [Context Engineering: How RAG, agents, and memory make LLMs actually useful](/blog/internal/context-engineering-modern-llm-ecosystem/)