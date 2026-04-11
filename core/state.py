from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AgentState:
    query: str

    memory: str = ""

    # 🧠 structured plan (IMPORTANT UPGRADE)
    plan: List[str] = field(default_factory=list)

    # 🔍 step-level execution trace
    step_outputs: List[Dict[str, Any]] = field(default_factory=list)

    # 🧠 final aggregated context
    context: str = ""

    answer: str = ""

    score: int = 0