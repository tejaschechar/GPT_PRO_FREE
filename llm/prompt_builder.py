def build_prompt(query: str, task: str, context: str = "", memory: str = "") -> str:

    if task == "coding":
        system = """
You are an expert software engineer.
- Write clean, correct code
- Explain only if needed
- Prefer efficient solutions
"""
    elif task == "math":
        system = """
You are a math expert.
- Solve step by step
- Show final answer clearly
"""
    else:
        system = """
You are a helpful AI assistant.
- Be clear and concise
"""

    return f"""
{system}

CONTEXT:
{context}

MEMORY:
{memory}

USER QUERY:
{query}

FINAL ANSWER:
"""