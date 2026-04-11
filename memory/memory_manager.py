_memory_store = {}

def get_memory(query: str):
    return _memory_store.get(query, "")

def save_memory(query: str, answer: str):
    _memory_store[query] = answer