from tools.math_solver import solve_math
from services.context_builder import build_context
from tools.python_exec import run_python_code
import re


def tool_router(step: str):

    step_lower = step.lower()

    # 🧮 1. MATH
    if any(sym in step for sym in ["=", "+", "-", "*", "/"]) or \
       re.search(r"\b(solve|derivative|integrate)\b", step_lower):

        return {
            "tool": "math",
            "result": solve_math(step)
        }

    # 🐍 2. PYTHON EXECUTION
    if "```python" in step_lower or step_lower.startswith("python:"):

        return {
            "tool": "python",
            "result": run_python_code(step)
        }

    # 🌐 3. SEARCH / REAL WORLD INFO
    search_keywords = [
        "latest", "news", "current", "price",
        "update", "who is", "what is", "today", "market", "bitcoin", "crypto"
    ]

    if any(k in step_lower for k in search_keywords):

        return {
            "tool": "search",
            "result": build_context(step)
        }

    # ❌ fallback
    return {
        "tool": "llm",
        "result": None
    }