from llm.multi_model_pipeline import multi_model_answer, creative_pipeline
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from llm.multi_model_pipeline import evaluate_answer
from services.context_builder import build_context
from tools.math_solver import solve_math
import re


MODEL_MAP = {
    "fast": "mistral:latest",
    "reasoning": "llama3:8b-instruct-q4_0",
    "creative": "dolphin-mistral:latest",
    "default": "llama3:8b-instruct-q4_0"
}


def parse_score(text: str) -> int:
    try:
        match = re.search(r"\d+", text)
        if match:
            return int(match.group())
    except:
        pass
    return 5



def should_search(query: str) -> bool:
    q = query.lower()

    # 🔹 High-signal keywords
    keywords = [
        "latest", "news", "today", "current",
        "price", "stock", "crypto", "market",
        "2024", "2025", "recent", "update"
    ]

    # 🔹 Pattern-based triggers
    patterns = [
        r"\b(today|now|currently)\b",
        r"\bprice of\b",
        r"\bstock of\b",
        r"\bwho is\b.*\b(current|now)\b"
    ]

    if any(k in q for k in keywords):
        return True

    if any(re.search(p, q) for p in patterns):
        return True

    return False

def summarize_context(context):
    return generate_response(
        "mistral:latest",
        f"Summarize this information clearly:\n{context}"
    )

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

def is_math_query(query: str) -> bool:
    return any(sym in query for sym in ["+", "-", "*", "/", "="]) or "solve" in query.lower()


def route_query(query: str, user_model: str = None, user_mode="auto", trace=False) -> str:

    print(f"\n[ROUTER] Query: {query}")

    # 🔹 Manual model override
    if user_model and user_model != "auto":
        prompt = build_prompt(query, "default")
        return generate_response(user_model, prompt)

    task_type = detect_task(query, user_mode)
    print(f"[ROUTER] Task: {task_type}")

    try:
        # 🧮 1. Math handling (optimized)
        if is_math_query(query):
            math_result = solve_math(query)

            if math_result:
                explanation = generate_response(
                    "llama3:8b-instruct-q4_0",
                    f"""
Explain this step-by-step clearly:

Query:
{query}

Result:
{math_result}
"""
                )
                return f"{math_result}\n\nExplanation:\n{explanation}"

        # 🧠 2. Multi-model mode
        if task_type == "multi":
            return multi_model_answer(query, trace=trace)

        # 🎨 3. Creative mode
        if task_type == "creative":
            return creative_pipeline(query)

        # 🌐 4. Search decision
        use_search = should_search(query)
        print(f"[ROUTER] Search used: {use_search}")

        context = ""
        if use_search:
            context = build_context(query, use_search=True)

        # 🧠 5. Context summarization + trimming
        if context and "No external context" not in context:
            context = summarize_context(context)
            context = context[:1000]  # limit size
        else:
            context = ""

        # 🧠 6. Context-aware model selection
        if context:
            model_name = "llama3:8b-instruct-q4_0"
        else:
            model_name = MODEL_MAP.get(task_type, MODEL_MAP["default"])

        print(f"[ROUTER] Using model: {model_name}")

        # 🧠 7. Generate answer
        prompt = build_prompt(query, task_type, context=context)
        answer = generate_response(model_name, prompt)

        # 🚨 8. Hallucination safety check
        if "i don't know" in answer.lower():
            print("[ROUTER] Model uncertain → fallback multi-model")
            return multi_model_answer(query)

        # ⚡ Skip evaluation for fast tasks
        if task_type == "fast":
            return answer

        # 🧠 9. Evaluation
        score_text = evaluate_answer(query, answer)
        score = parse_score(score_text)

        print(f"[ROUTER] Score: {score}")

        if score < 6 and user_mode != "multi":
            print("[ROUTER] Low confidence → multi-model fallback")
            return multi_model_answer(query)

        return answer

    except Exception as e:
        print("[ROUTER ERROR]:", e)
        return generate_response(
            MODEL_MAP["default"],
            build_prompt(query, "default")
        )