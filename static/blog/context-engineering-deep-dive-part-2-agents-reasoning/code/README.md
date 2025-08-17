# Context Engineering Deep Dive Part 2: Agents & Reasoning

## Code Examples

This directory contains Python code examples demonstrating the agent reasoning patterns covered in the blog post. All examples use the free `openai/gpt-oss-20b:free` model through [OpenRouter](https://openrouter.ai/openai/gpt-oss-20b:free/api).

## Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create `.env` file** with your OpenRouter API key:
   ```bash
   echo "OPENROUTER_API_KEY=your_api_key_here" > .env
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

## Running Examples

Each script demonstrates different agent reasoning patterns:

### 1. T-SQL to dbt Agent
```bash
uv run 1_tsql_to_dbt_agent.py
```
Single agent that analyzes T-SQL stored procedures and converts them to dbt models using step-by-step reasoning.

### 2. Multi-Agent Workflow
```bash
uv run 2_multi_agent_workflow.py
```
Demonstrates specialized agents collaborating on T-SQL to dbt migration with distinct reasoning capabilities.

## Environment Variables

Required environment variables in `.env`:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Related Blog Post

Read the full article: [Agents & Reasoning: How LLMs actually think through complex problems](https://about.datnguyen.de/blog/internal/context-engineering-deep-dive-part-2-agents-reasoning/)