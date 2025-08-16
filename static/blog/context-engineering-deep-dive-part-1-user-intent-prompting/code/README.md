# Context Engineering Deep Dive Part 1: User Intent & Prompting

## Code Examples

This directory contains Python code examples demonstrating the prompt engineering techniques covered in the blog post. All examples use the free `openai/gpt-oss-20b:free` model through [OpenRouter](https://openrouter.ai/openai/gpt-oss-20b:free/api).

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

Each script demonstrates different prompting techniques:

### 1. System vs User Prompts
```bash
uv run python 1_system_vs_user_prompts.py
```
Demonstrates the importance of separating system context from user requests.

### 2. Few-Shot Learning
```bash
uv run python 2_few_shot_learning.py
```
Shows how examples dramatically improve LLM performance compared to instructions alone.

### 3. Chain-of-Thought Reasoning
```bash
uv run python 3_chain_of_thought.py
```
Makes LLMs show their step-by-step reasoning for complex problems.

### 4. Role-Playing Prompts
```bash
uv run python 4_role_playing_prompts.py
```
Creates detailed expert personas for specialized analysis.

### 5. Constraint-Based Prompting
```bash
uv run python 5_constraint_based_prompting.py
```
Uses strict constraints to ensure consistent, reliable outputs.

### 6. Structured Output
```bash
uv run python 6_structured_output.py
```
Forces JSON-formatted responses instead of messy text outputs.

## Environment Variables

Required environment variables in `.env`:

```bash
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Related Blog Post

Read the full article: [User Intent & Prompting: Making LLMs understand what you really want](https://about.datnguyen.de/blog/internal/context-engineering-deep-dive-part-1-user-intent-prompting/)
