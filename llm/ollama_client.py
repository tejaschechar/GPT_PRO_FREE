from langchain_ollama import OllamaLLM
from functools import lru_cache


@lru_cache(maxsize=2)
def load_model(model_name: str):
    return OllamaLLM(model=model_name)


def generate_response(model_name: str, prompt: str) -> str:
    try:
        llm = load_model(model_name)
        return llm.invoke(prompt)

    except Exception as e:
        print("Error:", e)
        print("Fallback to mistral...")
        return load_model("mistral:latest").invoke(prompt)