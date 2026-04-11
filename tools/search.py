from ddgs import DDGS


def search_web(query: str, max_results=5):
    try:
        results = []
        seen = set()

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):

                title = (r.get("title") or "").strip()
                body = (r.get("body") or "").strip()
                link = (r.get("href") or "").strip()

                # 🔒 quality filter
                if len(body) < 50:
                    continue

                snippet = body[:800]  # tighter for LLM context

                key = (title[:50], snippet[:100])
                if key in seen:
                    continue
                seen.add(key)

                results.append({
                    "title": title,
                    "snippet": snippet,
                    "source": link
                })

        # ⚠️ explicit failure signal (IMPORTANT FOR AGENT)
        if not results:
            return [{
                "title": "No results found",
                "snippet": "Search returned no useful results.",
                "source": ""
            }]

        return results

    except Exception as e:
        return [{
            "title": "Search Error",
            "snippet": str(e),
            "source": ""
        }]