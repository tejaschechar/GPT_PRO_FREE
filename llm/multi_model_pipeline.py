from llm.ollama_client import generate_response

def multi_model_answer(query: str, trace=False):
    steps = []

    # 🧠 Step 1: Draft
    draft_prompt = f"""
You are a fast AI assistant.
Generate a quick, useful draft answer.

Question:
{query}

Draft Answer:
"""
    draft = generate_response("mistral:latest", draft_prompt)
    steps.append(("Draft (mistral)", draft))

    # 🧠 Step 2: Refine
    refine_prompt = f"""
You are an expert AI.
Improve the answer below:
- Make it more accurate
- Add missing details
- Improve clarity

Original Question:
{query}

Draft:
{draft}

Improved Answer:
"""
    refined = generate_response("llama3:8b-instruct-q4_0", refine_prompt)
    steps.append(("Refined (llama3)", refined))

    # 🧠 Step 3: Critic (VERY IMPORTANT)
    critic_prompt = f"""
You are a strict reviewer.

Check the answer for:
- factual errors
- logical mistakes
- missing important points

If correct → return improved version
If wrong → fix it

Question:
{query}

Answer:
{refined}

Final Answer:
"""
    final = generate_response("llama3:8b-instruct-q4_0", critic_prompt)
    steps.append(("Final (critic)", final))

    if trace:
        return steps

    return final

def creative_pipeline(query: str):

    creative_prompt = f"""
You are a creative AI.
Generate an engaging, imaginative response.

Prompt:
{query}

Creative Output:
"""
    creative = generate_response("dolphin-mistral:latest", creative_prompt)

    structure_prompt = f"""
You are a professional editor.

Convert this into:
- clear structure
- proper formatting
- easy readability

Content:
{creative}

Structured Output:
"""
    structured = generate_response("llama3:8b-instruct-q4_0", structure_prompt)

    return structured

def evaluate_answer(query, answer):
    prompt = f"""
Rate this answer from 1-10 based on accuracy.

Question:
{query}

Answer:
{answer}

Score only:
"""
    return generate_response("mistral:latest", prompt)