from memory.vector_store import VectorStore

store = VectorStore()


def save_memory(query: str, answer: str):
    # structured memory format (VERY IMPORTANT)
    text = f"Q: {query} | A: {answer}"
    
    store.add(text)
    store.save()   # 🔥 persist immediately


def get_memory(query: str, k=3):
    results = store.search(query, k=k)

    if not results:
        return ""

    # format memory nicely
    return "\n".join([f"- {r}" for r in results])