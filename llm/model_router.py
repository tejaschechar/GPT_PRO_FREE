import re

from llm.multi_model_pipeline import multi_model_answer, creative_pipeline, evaluate_answer
from llm.ollama_client import generate_response
from llm.prompt_builder import build_prompt
from services.context_builder import build_context
from tools.math_solver import solve_math

# 🧠 PHASE 3 MEMORY
from memory.memory_manager import get_memory, save_memory


MODEL_MAP = {
    "fast": "mistral:latest",
    "reasoning": "llama3:8b-instruct-q4_0",
    "creative": "dolphin-mistral:latest",
    "default": "llama3:8b-instruct-q4_0"
}


def parse_score(text: str) -> int:
    try:
        match = re.search(r"\d+", text)
        return int(match.group()) if match else 5
    except:
        return 5


def should_search(query: str) -> bool:
    q = query.lower()

    keywords = [
        "latest", "news", "today", "current",
        "price", "stock", "crypto", "market",
        "2024", "2025", "recent", "update"
    ]

    patterns = [
        r"\b(today|now|currently)\b",
        r"\bprice of\b",
        r"\bstock of\b",
        r"\bwho is\b.*\b(current|now)\b"
    ]

    return any(k in q for k in keywords) or any(re.search(p, q) for p in patterns)


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

    if any(k in q for k in ["code", "python", "algorithm", "leetcode"]):
        return "reasoning"

    if any(k in q for k in ["summarize", "short", "brief"]):
        return "fast"

    if any(k in q for k in ["explain deeply", "in detail", "why"]):
        return "reasoning"

    return "default"


def is_math_query(query: str) -> bool:
    return any(sym in query for sym in ["+", "-", "*", "/", "="]) or "solve" in query.lower()


def route_query(query: str, user_model: str = None, user_mode="auto", trace=False):

    print(f"\n[ROUTER] Query: {query}")

    # 🧠 MEMORY
    memory = get_memory(query)
    if memory:
        print("[ROUTER] Memory used")

    # 🔹 override
    if user_model and user_model != "auto":
        prompt = build_prompt(query, "default", context=memory)
        answer = generate_response(user_model, prompt)
        save_memory(query, answer)
        return answer

    task_type = detect_task(query, user_mode)
    print(f"[ROUTER] Task: {task_type}")

    try:

        # 🧮 MATH FIRST
        if is_math_query(query):
            result = solve_math(query)

            if result:
                explanation = generate_response(
                    "llama3:8b-instruct-q4_0",
                    f"Explain step-by-step:\n{query}\nResult: {result}"
                )

                final = f"{result}\n\nExplanation:\n{explanation}"
                save_memory(query, final)
                return final

        # 🧠 SPECIAL PIPELINES
        if task_type == "multi":
            answer = multi_model_answer(query, trace=trace)
            save_memory(query, answer)
            return answer

        if task_type == "creative":
            answer = creative_pipeline(query)
            save_memory(query, answer)
            return answer

        # 🌐 SEARCH
        use_search = should_search(query)
        print(f"[ROUTER] Search used: {use_search}")

        search_context = ""
        if use_search:
            search_context = build_context(query, use_search=True)

        # 🧠 FINAL CONTEXT BUILD (IMPORTANT FIX)
        final_context_parts = []

        if memory:
            final_context_parts.append(f"PAST MEMORY:\n{memory}")

        if search_context:
            final_context_parts.append(f"SOURCES:\n{search_context}")

        context = "\n\n".join(final_context_parts)

        # ⚡ DO NOT SUMMARIZE HERE ❌

        model_name = (
            "llama3:8b-instruct-q4_0"
            if context
            else MODEL_MAP.get(task_type, MODEL_MAP["default"])
        )

        print(f"[ROUTER] Using model: {model_name}")

        prompt = build_prompt(query, task_type, context=context)
        answer = generate_response(model_name, prompt)

        # 🚨 fallback
        if "i don't know" in answer.lower():
            print("[ROUTER] fallback triggered")
            answer = multi_model_answer(query, trace=trace)

        # ⚡ evaluation
        if task_type != "fast":
            score_text = evaluate_answer(query, answer)
            score = parse_score(score_text)

            print(f"[ROUTER] Score: {score}")

            if score < 6 and user_mode != "multi":
                print("[ROUTER] low confidence fallback")
                answer = multi_model_answer(query, trace=trace)

        # 💾 SAVE MEMORY
        save_memory(query, answer)

        return answer

    except Exception as e:
        print("[ROUTER ERROR]:", e)

        fallback = generate_response(
            MODEL_MAP["default"],
            build_prompt(query, "default", context=memory)
        )

        save_memory(query, fallback)
        return fallback