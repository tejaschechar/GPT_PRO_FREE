import re
from typing import Dict

def classify_intent(query: str) -> Dict:
    q = query.lower()

    intent = {
        "type": "general",
        "confidence": 0.0
    }

    # -------------------------
    # MATH (strong signal)
    # -------------------------
    if re.search(r"(solve|derivative|integrate|\\d+\\s*[\\+\\-\\*/])", q):
        intent["type"] = "math"
        intent["confidence"] = 0.95
        return intent

    # -------------------------
    # CODE
    # -------------------------
    if any(k in q for k in ["python", "code", "function", "algorithm"]):
        intent["type"] = "code"
        intent["confidence"] = 0.9
        return intent

    # -------------------------
    # FINANCE / MARKET
    # -------------------------
    finance_keywords = [
        "price", "bitcoin", "btc", "crypto", "stock",
        "market", "share", "nse", "sensex", "nasdaq"
    ]

    if any(k in q for k in finance_keywords):
        intent["type"] = "finance"
        intent["confidence"] = 0.85
        return intent

    # -------------------------
    # KNOWLEDGE / EXPLANATION
    # -------------------------
    if any(k in q for k in ["what is", "explain", "who is", "how does"]):
        intent["type"] = "knowledge"
        intent["confidence"] = 0.7
        return intent

    return intent