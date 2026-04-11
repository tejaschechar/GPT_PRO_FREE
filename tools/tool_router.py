from tools.math_solver import solve_math
from services.context_builder import build_context
from tools.python_exec import run_python_code
import re

def tool_router(step: str):

    step_lower = step.lower().strip()

    # -----------------------
    # 🐍 PYTHON (HIGHEST PRIORITY)
    # -----------------------
    if "```python" in step_lower or step_lower.startswith("python:"):
        return {
            "tool": "python",
            "confidence": 0.99,
            "result": run_python_code(step)
        }

    # -----------------------
    # 🧮 MATH (STRICT)
    # -----------------------
    math_patterns = [
        r"^\s*solve\b",
        r"^\s*derivative\b",
        r"^\s*integrate\b",
        r"^\s*\d+\s*[\+\-\*/]\s*\d+\s*$",
        r"^\s*[0-9x]+\s*=\s*[0-9x]+\s*$",
    ]

    if any(re.search(p, step_lower) for p in math_patterns):
        return {
            "tool": "math",
            "confidence": 0.95,
            "result": solve_math(step)
        }

    # -----------------------
    # 🌐 SEARCH
    # -----------------------
    search_keywords = [
        "latest", "news", "current", "price",
        "bitcoin", "crypto", "stock",
        "who is", "when did", "where is",
        "value", "rate", "market", "today"
    ]

    if any(k in step_lower for k in search_keywords):
        return {
            "tool": "search",
            "confidence": 0.85,
            "result": build_context(step)
        }

    # -----------------------
    # 🤖 LLM FALLBACK
    # -----------------------
    return {
        "tool": "llm",
        "confidence": 0.5,
        "result": None
    }