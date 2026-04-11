from llm.client import generate_response
import json
import re


def clean_json(response: str):
    """
    Extract JSON safely from LLM output
    """
    try:
        # remove markdown fences
        response = response.strip()
        response = re.sub(r"```.*?```", "", response, flags=re.DOTALL).strip()

        # extract JSON array
        start = response.find("[")
        end = response.rfind("]")

        if start == -1 or end == -1:
            return None

        json_str = response[start:end+1]
        return json.loads(json_str)

    except:
        return None


def planner_node(query: str, memory: str):

    prompt = f"""
You are a planning agent for an autonomous AI system.

Break the task into clear executable steps.

RULES:
- Output ONLY a JSON array
- Each step must be actionable
- Do NOT explain
- Do NOT include numbering or text
- Each step should be 1 clear action

FORMAT:
["step1", "step2", "step3"]

QUERY:
{query}

MEMORY:
{memory}
"""

    response = generate_response("llama3:8b-instruct-q4_0", prompt)

    plan = clean_json(response)

    # 🔒 fallback safety
    if not plan or len(plan) == 0:
        return [query]

    return plan