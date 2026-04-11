from tools.search import search_web


def format_results(results):
    formatted = []
    seen = set()

    for i, r in enumerate(results, 1):
        title = (r.get("title") or "").strip()
        snippet = (r.get("snippet") or "").strip()
        source = (r.get("source") or "").strip()

        # skip garbage results
        if len(snippet) < 20:
            continue

        key = (title[:50], snippet[:100])
        if key in seen:
            continue
        seen.add(key)

        formatted.append(f"[{i}] {title}\n{snippet}\nSource: {source}")

    return "\n\n".join(formatted)


def build_context(query: str, max_chars: int = 5000, use_search: bool = True):

    if not query or not query.strip():
        return "Question: (empty query)"

    context = ""

    if use_search:
        results = search_web(query) or []

        if len(results) == 0:
            return f"Question: {query}\n\nNo reliable sources found."

        context = format_results(results)[:max_chars]

    if context.strip():
        return f"""
You are an AI assistant that answers ONLY using verified sources.

Question:
{query}

Sources:
{context}

Instructions:
- Use ONLY provided sources
- Be factual
- Add citations like [1], [2]
- If insufficient info → say "I don't know"
""".strip()

    return f"Question: {query}"