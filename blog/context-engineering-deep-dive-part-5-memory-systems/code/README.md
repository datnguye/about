# Memory Systems Code Examples

This directory contains executable code examples for the "Memory Systems" article in the Context Engineering Deep Dive series.

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

Each script demonstrates a specific memory system concept:

```bash
# Basic conversation memory with token counting and smart trimming
uv run 1_conversation_memory.py

# Entity tracking across conversations with importance scoring
uv run 2_entity_memory.py

# Semantic memory with vector embeddings and similarity search
uv run 3_vector_memory.py

# Production-ready hybrid memory system (Hot/Warm/Cold architecture)
uv run 4_hybrid_memory_system.py

# Privacy-compliant memory with GDPR features
uv run 6_privacy_compliant_memory.py
```

## Generated Outputs

All LLM responses are saved in the `llm_response/` directory for reference and verification.

## Dependencies

- **sentence-transformers**: Text embeddings for semantic similarity
- **numpy**: Numerical operations for vector calculations
- **tiktoken**: Token counting for conversation memory
- **python-dotenv**: Environment variable management (for scripts that need API keys)
- **litellm**: Unified LLM API interface (for scripts that make API calls)

Note: Some scripts use simplified implementations that don't require external services, making them easy to run locally.

## Model Used

All examples use the `gpt-oss-20b:free` model via OpenRouter API, keeping costs minimal while demonstrating production patterns.