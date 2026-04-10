from duckduckgo_search import DDGS


def search_web(query: str, max_results=5) -> str:
    try:
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get("title", "")
                body = r.get("body", "")
                link = r.get("href", "")

                if body:
                    results.append(f"- {title}\n  {body[:3000]}\n  Source: {link}")

        if not results:
            return "No relevant results found."

        return "\n\n".join(results)

    except Exception as e:
        print("[SEARCH ERROR]:", e)
        return "Search failed."