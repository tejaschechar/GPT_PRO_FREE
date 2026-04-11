from llm.client import generate_response
import re


def parse_score(text: str) -> int:
    try:
        match = re.search(r"\b([1-9]|10)\b", text)
        if not match:
            return 5

        score = int(match.group())

        # 🔒 clamp range
        return max(1, min(10, score))

    except:
        return 5


def critic_node(query: str, answer: str):

    prompt = f"""
You are a strict AI evaluator.

Rate the answer from 1 to 10 based on:
- correctness
- clarity
- completeness

RULES:
- Return ONLY a single number (1-10)
- No explanation
- No text

QUESTION:
{query}

ANSWER:
{answer}

SCORE:
"""

    score_text = generate_response("llama3:8b-instruct-q4_0", prompt)

    score = parse_score(score_text)

    # 🔒 safety fallback
    if score is None:
        return 5

    return score