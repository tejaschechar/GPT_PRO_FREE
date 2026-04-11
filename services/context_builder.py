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


def build_context(query: str, max_chars: int = 5000):

    # 🌐 Always fetch inside this layer (single responsibility)
    results = search_web(query)

    if not results:
        return f"""
Question: {query}

No reliable sources found.
Respond with: "I don't know"
"""

    combined = format_results(results)

    # ✂️ safer truncation (line-aware, not raw slicing)
    lines = combined.split("\n")
    trimmed = []
    total = 0

    for line in lines:
        total += len(line)
        if total > max_chars:
            break
        trimmed.append(line)

    context = "\n".join(trimmed)

    return f"""
You are an AI assistant that answers using VERIFIED sources.

Question:
{query}

Sources:
{context}

Instructions:
- Use ONLY the sources
- Cite using [1], [2]
- Do not hallucinate
- If missing info, say "I don't know"
"""