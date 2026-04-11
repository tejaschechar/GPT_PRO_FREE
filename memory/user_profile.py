import json
import os
from collections import defaultdict

PROFILE_PATH = "data/user_profile.json"


def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)

    return {
        "interests": {},
        "preferences": {},
        "history": []
    }


def save_profile(profile):
    os.makedirs("data", exist_ok=True)

    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)


def update_preferences(query: str, response: str = None):
    profile = load_profile()
    q = query.lower()

    # 🔥 simple signal extraction (can later replace with LLM extractor)
    signals = {
        "python": "programming",
        "ai": "technology",
        "anime": "entertainment",
        "finance": "finance",
        "cricket": "sports"
    }

    for keyword, category in signals.items():
        if keyword in q:
            profile["interests"][category] = profile["interests"].get(category, 0) + 1

    # store conversation history (important for future memory systems)
    profile["history"].append({
        "query": query,
        "response": response
    })

    # limit memory size (VERY IMPORTANT)
    profile["history"] = profile["history"][-50:]

    save_profile(profile)


def get_preferences():
    return load_profile()