import sys
import os

# 🔥 FIX: ensure project root is in path FIRST
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.graph import run_graph


def main():
    print("🚀 V2 AI Agent System Running")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        result = run_graph(query)

        print("\nAI:", result)
        print("-" * 50)


if __name__ == "__main__":
    main()