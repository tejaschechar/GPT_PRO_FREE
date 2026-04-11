import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm.model_router import route_query


# 📊 Tracking results
results_summary = []


def test_case(name, query, **kwargs):
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"[QUERY] {query}")

    start = time.time()

    try:
        result = route_query(query, **kwargs)
        status = "SUCCESS"

    except Exception as e:
        result = str(e)
        status = "FAILED"

    end = time.time()

    duration = round(end - start, 2)

    print("\n[RESULT]")
    print(result)

    print(f"\n[Time Taken]: {duration} sec")
    print(f"[Status]: {status}")

    results_summary.append({
        "name": name,
        "status": status,
        "time": duration
    })


def run_tests():

    '''# 🧠 Basic
    test_case("Normal question", "What is machine learning?")'''

    # 💻 Multi-model reasoning
    test_case(
        "Coding (multi-model)",
        "Write Python code for binary search",
        user_mode="multi"
    )

    '''# ⚡ Fast task
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

    # 🧮 Math tests
    test_case("Math calculation", "234 * 567")
    test_case("Equation solving", "x^2 - 4 = 0")
    test_case("Derivative", "derivative of x^2 + 3*x")
    test_case("Integration", "integrate x^2 + 2*x")
    '''
    # 🌐 Search queries
    test_case("Search (latest info)", "latest AI news today")
    test_case("Search (price query)", "current bitcoin price")

    '''# 🎨 Creative
    test_case(
        "Creative writing",
        "Write a short story about an AI that becomes human"
    )

    # 🧠 Deep reasoning
    test_case(
        "Deep explanation",
        "Explain quantum computing in detail"
    )

    # ⚠️ Edge case
    test_case(
        "Unknown / tricky",
        "Who is the current king of Mars?"
    )

    # 🔥 Complex reasoning
    test_case(
        "Long complex query",
        "Explain how neural networks work and compare them with decision trees in detail"
    )

    # 🔍 Multi-model trace mode
    test_case(
        "Multi-model with trace",
        "Explain blockchain in detail",
        user_mode="multi",
        trace=True
    )'''


def performance_test():
    print(f"\n{'='*70}")
    print("PERFORMANCE TEST")
    print(f"{'='*70}")

    query = "Explain machine learning"

    start = time.time()
    route_query(query)
    end = time.time()

    print(f"[Time Taken]: {round(end - start, 2)} sec")


def print_summary():
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}")

    success = sum(1 for r in results_summary if r["status"] == "SUCCESS")
    failed = sum(1 for r in results_summary if r["status"] == "FAILED")
    avg_time = sum(r["time"] for r in results_summary) / len(results_summary)

    print(f"Total Tests: {len(results_summary)}")
    print(f"Success: {success}")
    print(f"Failed: {failed}")
    print(f"Avg Time: {round(avg_time, 2)} sec")


if __name__ == "__main__":
    run_tests()
    performance_test()
    print_summary()