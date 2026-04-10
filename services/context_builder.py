from tools.search import search_web


def format_results(results):
    formatted = []

    for i, r in enumerate(results, 1):
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        source = r.get("source", "")

        formatted.append(
            f"[{i}] {title}\n{snippet}\nSource: {source}"
        )

    return "\n\n".join(formatted)


def build_context(query: str, use_search=False, max_chars=5000):
    context = ""

    if use_search:
        results = search_web(query)

        if not results:
            return f"""
Question: {query}

No reliable sources found.
Say "I don't know" if unsure.
"""

        # ✅ Convert dict → string
        combined = format_results(results)

        # ✂️ Trim context (VERY IMPORTANT)
        context = combined[:max_chars]

    if context:
        context = f"""
You are an AI assistant that answers using VERIFIED sources.

Question:
{query}

Sources:
{context}

Instructions:
- Answer using ONLY the sources
- Add citations like [1], [2]
- Be concise and factual
- If unsure, say "I don't know"
"""
    else:
        context = f"Question: {query}"

    return context