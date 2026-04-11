from llm.client import generate_response
from tools.tool_router import tool_router


def executor_node(step: str, context: str):

    tool_result = tool_router(step)

    # 🔒 normalize tool output (VERY IMPORTANT)
    if isinstance(tool_result, dict):
        tool_result = str(tool_result)
    elif tool_result is None:
        tool_result = "No tool used"
    else:
        tool_result = str(tool_result)

    prompt = f"""
You are an execution agent in a multi-step AI system.

IMPORTANT RULES:
- If TOOL RESULT is present, prioritize it over CONTEXT
- Do NOT ignore tool output
- Be precise and do not hallucinate

STEP:
{step}

CONTEXT:
{context}

TOOL RESULT:
{tool_result}

FINAL ANSWER:
"""

    return generate_response("llama3:8b-instruct-q4_0", prompt)