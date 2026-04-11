import subprocess
import logging


def generate_response(model: str, prompt: str, timeout: int = 60) -> str:

    try:
        # 🔥 prevent runaway prompts
        prompt = prompt[:12000]

        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=False,
            timeout=timeout
        )

        # 🔥 decode safely (stdout + stderr)
        output = result.stdout.decode("utf-8", errors="ignore").strip()
        error = result.stderr.decode("utf-8", errors="ignore").strip()

        if result.returncode != 0:
            logging.error(f"LLM ERROR: {error}")
            return "Error: LLM failed"

        if not output:
            return "Error: Empty response"

        # 🔥 limit response size (important for agent stability)
        return output[:8000]

    except subprocess.TimeoutExpired:
        return "Error: Timeout"

    except Exception as e:
        logging.error(str(e))
        return f"Error: {str(e)}"