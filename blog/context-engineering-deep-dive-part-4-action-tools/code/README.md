# Action Tools Code Examples

This directory contains executable code examples for the "Action Tools" article in the Context Engineering Deep Dive series.

## Setup

1. **Get your API key**: Sign up at [OpenRouter](https://openrouter.ai/) for free access to various LLM models
2. **Set environment variable**: Create a `.env` file with your API key:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
3. **Install dependencies**: All dependencies are managed with `uv`
   ```bash
   uv sync
   ```

## Running Examples

Each script demonstrates a specific action tools concept:

```bash
# Evolution of function calling from JSON to structured outputs
uv run 1_function_calling_evolution.py

# Safe tool interfaces with validation and error handling
uv run 2_safe_tool_interfaces.py

# Different categories of tools: Read, Write, Compute, External
uv run 3_tool_categories.py

# LangChain toolkit integration patterns
uv run 4_langchain_toolkit.py

# Model Control Protocol (MCP) examples
uv run 5_mcp_example.py
```

## Generated Outputs

All LLM responses are saved in the `llm_response/` directory for reference and verification.

## Dependencies

- **litellm**: Unified LLM API interface for function calling
- **python-dotenv**: Environment variable management
- **langchain**: Tool ecosystem and agent frameworks
- **pydantic**: Data validation and schema management
- **requests**: HTTP client for external API tools

Note: Examples include production-ready safety patterns like input validation, permission checks, and audit logging.

## Model Used

All examples use the `gpt-oss-20b:free` model via OpenRouter API, keeping costs minimal while demonstrating production patterns.