=== Conversation Memory Demo ===
Token limit: 1000

--- Turn 1 ---
Messages: 3, Tokens: 29

--- Turn 2 ---
Messages: 5, Tokens: 53

--- Turn 3 ---
Messages: 7, Tokens: 76

--- Turn 4 ---
Messages: 9, Tokens: 109

--- Turn 5 ---
Messages: 11, Tokens: 136

--- Turn 6 ---
Messages: 13, Tokens: 161

--- Turn 7 ---
Messages: 15, Tokens: 175

=== Final Context ===
1. ⚙️ system: You are a helpful coding assistant specializing in...
2. 👤 user: Help me debug this Python function
3. 🤖 assistant: I'd be happy to help! Please share the function co...
4. 👤 user: def calculate_sum(numbers): return sum(numbers)
5. 🤖 assistant: That function looks correct! It calculates the sum...
6. 👤 user: It's giving me a TypeError
7. 🤖 assistant: The TypeError suggests you might be passing incomp...
8. 👤 user: TypeError: unsupported operand type(s) for +: 'int...
9. 🤖 assistant: Ah! You have strings mixed with integers. Try conv...
10. 👤 user: How do I convert strings to integers?
11. 🤖 assistant: Use int() function: int('5') converts string '5' t...
12. 👤 user: What about handling non-numeric strings?
13. 🤖 assistant: Use try/except with ValueError: try: int(x) except...
14. 👤 user: Show me a complete example
15. 🤖 assistant: Here's a robust version with error handling...

Final token count: 175

==================================================


[1;31mGive Feedback / Get Help: https://github.com/BerriAI/litellm/issues/new[0m
LiteLLM.Info: If you need to debug this error, use `litellm._turn_on_debug()'.

LLM test failed: litellm.NotFoundError: NotFoundError: OpenrouterException - {"error":{"message":"No endpoints found for openai/gpt-oss-20b:free.","code":404},"user_id":"user_31M7VppPHV2NEFvtpnCzwY0BELg"}
Make sure you have OPENROUTER_API_KEY set in your .env file
