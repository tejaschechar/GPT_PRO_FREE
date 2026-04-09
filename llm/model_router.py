from llm.multi_model_pipeline import multi_model_answer, creative_pipeline
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from llm.multi_model_pipeline import evaluate_answer

MODEL_MAP = {
    "fast": "mistral:latest",
    "reasoning": "llama3:8b-instruct-q4_0",
    "creative": "dolphin-mistral:latest",
    "default": "llama3:8b-instruct-q4_0"
}

def detect_task(query: str, user_mode="auto") -> str:
    q = query.lower()

    if user_mode == "multi":
        return "multi"

    if any(k in q for k in ["story", "write", "imagine", "creative"]):
        return "creative"

    elif any(k in q for k in ["code", "python", "algorithm", "leetcode"]):
        return "reasoning"

    elif any(k in q for k in ["summarize", "short", "brief"]):
        return "fast"

    elif any(k in q for k in ["explain deeply", "in detail", "why"]):
        return "reasoning"

    return "default"


def route_query(query: str, user_model: str = None, user_mode="auto") -> str:

    print(f"\n[ROUTER] Query: {query}")

    if user_model and user_model != "auto":
        print(f"[ROUTER] Manual model override: {user_model}")
        prompt = build_prompt(query, "default")
        return generate_response(user_model, prompt)

    task_type = detect_task(query, user_mode)
    print(f"[ROUTER] Task: {task_type}")

    try:
        if task_type == "multi":
            return multi_model_answer(query)

        if task_type == "creative":
            return creative_pipeline(query)

        model_name = MODEL_MAP.get(task_type, MODEL_MAP["default"])
        print(f"[ROUTER] Model: {model_name}")

        prompt = build_prompt(query, task_type)
        answer = generate_response(model_name, prompt)

        # 🧠 Quality check
        score = evaluate_answer(query, answer)

        try:
            score = int(score.strip())
        except:
            score = 5

        if score < 6:
            print("[ROUTER] Low confidence → retrying with multi-model")
            return multi_model_answer(query)

        return answer

    except Exception as e:
        print("[ROUTER] Error:", e)
        return generate_response(MODEL_MAP["default"], build_prompt(query, "default"))