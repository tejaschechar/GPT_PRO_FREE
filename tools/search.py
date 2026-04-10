from ddgs import DDGS


def search_web(query: str, max_results=5):
    try:
        results = []
        seen = set()

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                title = r.get("title", "").strip()
                body = r.get("body", "").strip()
                link = r.get("href", "").strip()

                if not body or len(body) < 50:
                    continue

                snippet = body[:3000]

                key = (title[:50], snippet)
                if key in seen:
                    continue
                seen.add(key)

                results.append({
                    "title": title,
                    "snippet": snippet,
                    "source": link
                })

        return results

    except Exception as e:
        print("[SEARCH ERROR]:", e)
        return []