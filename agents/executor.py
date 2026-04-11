from llm.client import generate_response
from tools.tool_router import tool_router
import json


def compute_confidence(tool_type, valid):
    base = {
        "math": 0.95,
        "python": 0.9,
        "search": 0.85,
        "llm": 0.6
    }.get(tool_type, 0.5)

    if not valid:
        return base * 0.3

    return base

def is_valid_tool_output(tool_type, tool_value):

    if tool_value is None:
        return False

    if isinstance(tool_value, dict):
        if tool_value.get("error"):
            return False
        if not tool_value.get("output") and not tool_value.get("result"):
            return False

    if isinstance(tool_value, str):
        err_signals = [
            "error",
            "exception",
            "traceback",
            "math error",
            "syntaxerror",
            "failed",
            "invalid"
        ]

        low = tool_value.lower()

        if any(e in low for e in err_signals):
            return False

        if tool_value.strip() == "":
            return False

    return True



def executor_node(step: str, context: str):

    tool_result = tool_router(step)

    tool_type = tool_result.get("tool", "llm")
    tool_value = tool_result.get("result")

    valid = is_valid_tool_output(tool_type, tool_value)
    confidence = compute_confidence(tool_type, valid)

    tool_payload = {
        "tool": tool_type,
        "result": tool_value,
        "valid": valid,
        "confidence": confidence
    }

    prompt = f"""
You are an execution engine.

RULES:
- TOOL_RESULT is SYSTEM OUTPUT (do not evaluate it)
- If TOOL_RESULT.valid = true → use it directly
- If false → fallback to reasoning
- Never modify tool output
- Be concise

STEP:
{step}

CONTEXT:
{context}

TOOL_RESULT:
{json.dumps(tool_payload, indent=2)}

FINAL ANSWER:
"""

    return generate_response("llama3:8b-instruct-q4_0", prompt)