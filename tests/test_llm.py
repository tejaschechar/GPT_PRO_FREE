import os
import sys
import time

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.model_router import route_query


def test_case(name, query, **kwargs):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"[QUERY] {query}")

    start = time.time()
    result = route_query(query, **kwargs)
    end = time.time()

    print("\n[RESULT]")
    print(result)

    print(f"\n[Time Taken]: {end - start:.2f} sec")


def run_tests():

    '''# 🧠 Basic
    test_case(
        "Normal question",
        "What is machine learning?"
    )

    # 💻 Multi-model reasoning
    test_case(
        "Coding (multi-model)",
        "Write Python code for binary search",
        user_mode="multi"
    )

    # ⚡ Fast task
    test_case(
        "Summarization",
        "Summarize artificial intelligence in short"
    )

    # 🎯 Manual override
    test_case(
        "Manual override",
        "Explain deep learning",
        user_model="mistral:latest"
    )

    # 🧮 Math tests (CRITICAL)
    test_case(
        "Math calculation",
        "234 * 567"
    )

    test_case(
        "Equation solving",
        "x^2 - 4 = 0"
    )

    test_case(
        "Derivative",
        "derivative of x^2 + 3*x"
    )

    test_case(
        "Integration",
        "integrate x^2 + 2*x"
    )'''

    # 🌐 Search-based queries
    test_case(
        "Search (latest info)",
        "latest AI news today"
    )

    test_case(
        "Search (price query)",
        "current bitcoin price"
    )

    '''# 🎨 Creative mode
    test_case(
        "Creative writing",
        "Write a short story about an AI that becomes human"
    )

    # 🧠 Deep reasoning
    test_case(
        "Deep explanation",
        "Explain quantum computing in detail"
    )

    # ⚠️ Edge cases
    test_case(
        "Unknown / tricky",
        "Who is the current king of Mars?"
    )

    # 🔥 Long complex query (should trigger better reasoning)
    test_case(
        "Long complex query",
        "Explain how neural networks work and compare them with decision trees in detail"
    )

    # 🔍 Multi-model with trace (DEBUG MODE)
    test_case(
        "Multi-model with trace",
        "Explain blockchain in detail",
        user_mode="multi",
        trace=True
    )'''


def performance_test():
    print(f"\n{'='*60}")
    print("PERFORMANCE TEST")
    print(f"{'='*60}")

    query = "Explain machine learning"

    start = time.time()
    route_query(query)
    end = time.time()

    print(f"[Time Taken]: {end - start:.2f} sec")


if __name__ == "__main__":
    run_tests()
    performance_test()