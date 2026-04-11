from core.state import AgentState
from agents.planner import planner_node
from agents.executor import executor_node
from agents.critic import critic_node
from memory.memory_manager import get_memory, save_memory


def run_graph(query: str):

    state = AgentState(query=query)

    # 🧠 MEMORY
    state.memory = get_memory(query)

    # 🧠 PLANNER (structured steps)
    state.plan = planner_node(state.query, state.memory)

    step_outputs = []

    # ⚙️ EXECUTION LOOP (FIXED)
    for step in state.plan:

        output = executor_node(step, state.context)

        # 🔒 store step-wise output (IMPORTANT FIX)
        step_outputs.append({
            "step": step,
            "output": output
        })

        # optional context growth (controlled)
        state.context = output  # instead of accumulation

    # 🧠 FINAL ANSWER
    state.answer = "\n\n".join([s["output"] for s in step_outputs])

    # 🔍 CRITIC
    state.score = critic_node(state.query, state.answer)

    # 🔁 IMPROVEMENT LOOP (better version)
    if state.score < 7:

        feedback_prompt = f"""
Improve the answer based on evaluation.

Original Query:
{query}

Current Answer:
{state.answer}

Critic Score:
{state.score}

Return improved answer.
"""

        state.answer = executor_node(feedback_prompt, "")

    # 💾 MEMORY
    save_memory(state.query, state.answer)

    return state.answer