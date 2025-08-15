+++
title = "Action Tools: How LLMs Finally Learned to Stop Talking and Start Doing"
description = "An LLM that can only generate text is like a brilliant consultant who can't touch a keyboard. Function calling changed everything — now your AI can ship code, query databases, and send emails."
date = 2025-01-19
template = "blog_page.html"

[extra]
author = "Dat Nguyen"
tags = ["LLM-Tools", "FunctionCalling", "API-Integration", "Automation", "LangChain", "OpenAI"]
read_time = "9 min read"
featured_image = "/blog/context-engineering-deep-dive-part-4-action-tools/hero.png"
toc = true
show_ads = true

enable_auto_related = true
+++

An LLM that can only generate text is like a brilliant consultant who can't touch a keyboard. Sure, they have great ideas, but someone else has to do the actual work. Function calling changed everything — now your AI can actually ship code, query databases, and send emails. Is it safe? That's... another question.

<!-- more -->

## The Game Changer Nobody Saw Coming

Remember when we had to parse LLM outputs with regex to trigger actions? Dark times. Now, models can directly call functions, use tools, and interact with the real world. The implications? Massive.

## Article Structure

### 1. **From Text to Action: The Evolution**
- The pre-function era (parsing JSON from prompts)
- OpenAI's function calling revolution
- Tool use vs function calling: what's the difference?

### 2. **Building Safe Tool Interfaces**
```python
from typing import Literal
from pydantic import BaseModel, Field

class DatabaseQuery(BaseModel):
    """Tool for read-only database queries"""
    query: str = Field(description="SQL query to execute")
    database: Literal["prod", "staging"] = Field(
        default="staging",
        description="Target database"
    )
    
    def validate_query(self):
        # No DELETE, UPDATE, DROP allowed
        dangerous_keywords = ['DELETE', 'UPDATE', 'DROP', 'ALTER']
        if any(keyword in self.query.upper() for keyword in dangerous_keywords):
            raise ValueError("Destructive operations not allowed")
```

### 3. **Tool Categories That Matter**
- **Data Tools**: SQL, APIs, file operations
- **Communication Tools**: Email, Slack, notifications
- **Development Tools**: Git, code execution, testing
- **Monitoring Tools**: Logs, metrics, alerts

### 4. **The LangChain Toolkit Approach**
```python
from langchain.tools import Tool, SQLDatabaseToolkit
from langchain.agents import create_sql_agent

# Building a complete toolkit
toolkit = SQLDatabaseToolkit(
    db=database,
    llm=llm,
    use_query_checker=True  # Double-check before execution
)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)
```

### 5. **Real-World Implementation: DevOps Assistant**
```python
class DevOpsAgent:
    def __init__(self):
        self.tools = {
            'check_server_status': self.check_status,
            'restart_service': self.restart_service,
            'analyze_logs': self.analyze_logs,
            'create_jira_ticket': self.create_ticket
        }
    
    @require_confirmation  # Human in the loop for dangerous ops
    def restart_service(self, service_name: str):
        # Implementation with safety checks
        pass
```

### 6. **Tool Orchestration Patterns**
- Sequential execution
- Parallel tool calls
- Conditional tool chains
- Retry mechanisms with exponential backoff

### 7. **Security & Safety Considerations**
- Input sanitization is NOT optional
- Rate limiting saves your wallet
- Audit logs for compliance
- Human-in-the-loop for critical operations

### 8. **Error Handling That Works**
```python
class ToolExecutor:
    def execute_with_fallback(self, tool, params):
        try:
            return tool.execute(params)
        except RateLimitError:
            # Backoff and retry
            time.sleep(2 ** attempt)
        except AuthenticationError:
            # Refresh credentials
            self.refresh_auth()
        except Exception as e:
            # Log and fallback to manual
            return {
                "error": str(e),
                "fallback": "Manual intervention required"
            }
```

### 9. **Performance Optimization**
- Tool response caching
- Batch operations where possible
- Async execution patterns
- Connection pooling strategies

## The Dangerous Part Nobody Mentions

Give an LLM database write access? Email sending capabilities? Code execution? Each tool is a potential footgun. Here's how to not shoot yourself:

1. **Principle of Least Privilege**: Read-only by default
2. **Validation Everything**: Never trust LLM-generated parameters
3. **Audit Everything**: If it's not logged, it didn't happen
4. **Circuit Breakers**: Automatic shutoff for suspicious patterns

## What's Actually Working

After implementing tools in production:
- Readonly tools first, always
- Human confirmation for state changes
- Comprehensive error handling
- Clear tool descriptions (the LLM needs to understand them)

## Metrics That Matter

- Tool call success rate
- Average execution time
- Error rate by tool type
- Cost per action

## Up Next

Your agents can think, access knowledge, and take actions. But what about remembering what happened 5 minutes ago? Or last week? Time to dive into memory systems...

---

*Technical deep dive series — Part 4 of 5*

**[← Part 3: RAG Systems](/blog/internal/context-engineering-deep-dive-part-3-rag-systems/)** | **[Part 5: Memory Systems →](/blog/internal/context-engineering-deep-dive-part-5-memory-systems/)**

## Related Articles in This Series

📚 **Context Engineering Deep Dive Series:**

1. [User Intent & Prompting: The Art of Making LLMs Understand What You Really Want](/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)
2. [Agents & Reasoning: When LLMs Learn to Think Before They Speak](/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)
3. [RAG Systems: When Your LLM Needs to Phone a Friend](/blog/internal/context-engineering-deep-dive-part-3-rag-systems/)
4. **Action Tools** (You are here)
5. [Memory Systems: Teaching LLMs to Remember (Without Going Broke)](/blog/internal/context-engineering-deep-dive-part-5-memory-systems/)

🎯 **Start with the overview:** [Context Engineering: How RAG, agents, and memory make LLMs actually useful](/blog/internal/context-engineering-modern-llm-ecosystem/)