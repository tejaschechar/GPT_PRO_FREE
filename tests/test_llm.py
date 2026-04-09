import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.model_router import route_query

def test_case(name, query, **kwargs):
    print(f"\n{'='*50}")
    print(f"TEST: {name}")
    print(f"{'='*50}")
    result = route_query(query, **kwargs)
    print("\n[RESULT]")
    print(result)

def run_tests():

    test_case(
        "Normal question",
        "What is machine learning?"
    )

    test_case(
        "Coding (multi-model)",
        "Write Python code for binary search",
        user_mode="multi"
    )

    test_case(
        "Summarization",
        "Summarize AI in short"
    )

    test_case(
        "Manual override",
        "Explain deep learning",
        user_model="mistral:latest"
    )


if __name__ == "__main__":
    run_tests()