import sys
import os

# 🔥 FIX: ALWAYS FIRST (before any project imports)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.graph import run_graph
from tools.search import search_web
from tools.math_solver import solve_math
from tools.python_exec import run_python_code
from services.context_builder import build_context
from memory.memory_manager import get_memory, save_memory


TEST_CASES = [
    # 🧠 Knowledge
    "What is AI?",
    "Explain reinforcement learning",
    "Explain transformers",

    # 🧮 Math
    "Solve 2x + 10 = 30",
    "Derivative of x^3 + 2x",
    "Integrate x^2",

    # 🌐 Search
    "What is the price of Bitcoin today in INR?",
    "Latest news about AI agents",

    # 💻 Coding
    "Write python code for merge sort",
    "Write python code for binary search",

    # 🧠 Compare
    "Compare CNN vs RNN with examples",

    # 🧪 Edge cases
    "!!!!!",
    "",
    "Solve everything in universe"
]


def run_full_test():
    print("\n🧪 STARTING V2 SYSTEM TESTS\n")
    print("=" * 60)

    passed = 0
    failed = 0

    for i, query in enumerate(TEST_CASES, 1):

        print(f"\n🧪 TEST {i}")
        print(f"QUERY: {query}")

        try:
            result = run_graph(query)

            print("\n🧠 OUTPUT:")
            print(result[:1200])

            if result and len(result) > 10:
                print("✅ PASS")
                passed += 1
            else:
                print("❌ FAIL")
                failed += 1

        except Exception as e:
            print("❌ ERROR:", e)
            failed += 1

        print("-" * 60)

    print("\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Total: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(TEST_CASES))*100:.2f}%")


def test_tools_directly():

    print("\n🧪 TOOL TESTS")
    print("=" * 60)

    print("\n🧮 Math Test:")
    print(solve_math("2x + 10 = 30"))

    print("\n🐍 Python Test:")
    print(run_python_code("print('Hello from sandbox')"))

    print("\n🌐 Search Test:")
    print(search_web("What is AI?")[:2])

    print("\n📚 Context Test:")
    print(build_context("AI agents latest news", use_search=True)[:500])

    print("\n🧠 Memory Test:")
    save_memory("hello", "world")
    print(get_memory("hello"))


if __name__ == "__main__":
    run_full_test()
    test_tools_directly()