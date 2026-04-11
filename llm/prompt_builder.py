def build_prompt(query: str, task: str, context: str = "", memory: str = "") -> str:

    system_map = {
        "coding": """
You are an expert software engineer.
- Write clean, correct, production-ready code
- Prefer efficiency and clarity
- If needed, explain briefly
""",

        "math": """
You are a math expert.
- Solve step by step
- Show final answer clearly
""",

        "reasoning": """
You are a strong reasoning AI agent.
- Think step by step
- Use logic and structured reasoning
- Be accurate and detailed
""",

        "creative": """
You are a creative assistant.
- Be imaginative
- Write engaging and original content
""",

        "fast": """
You are a fast response assistant.
- Be very concise
- Give direct answers only
""",

        "default": """
You are a helpful AI assistant.
- Be clear, accurate, and helpful
"""
    }

    system = system_map.get(task, system_map["default"])

    return f"""
{system}

IMPORTANT:
- You may receive TOOL OUTPUT inside context
- Always prioritize TOOL RESULTS if present
- Use MEMORY only if relevant

CONTEXT:
{context}

MEMORY:
{memory}

USER QUERY:
{query}

FINAL ANSWER:
"""