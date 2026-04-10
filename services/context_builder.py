from tools.search import search_web


def build_context(query: str, use_search=False, max_chars=1500):
    context = ""

    if use_search:
        results = search_web(query)

        if isinstance(results, list):
            combined = "\n\n".join(results)
        else:
            combined = results  # already formatted string

        # ✂️ Trim context (VERY IMPORTANT)
        context = combined[:max_chars]

    if context:
        context = f"""
RELEVANT INFORMATION:
{context}

INSTRUCTIONS:
- Use this information to answer the question
- If insufficient, say "I don't know"
"""
    else:
        context = "No external context provided."

    return context