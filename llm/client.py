import subprocess
import logging


def generate_response(model: str, prompt: str, timeout: int = 60) -> str:

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=False,  # 🔥 IMPORTANT FIX
            timeout=timeout
        )

        if result.returncode != 0:
            logging.error(result.stderr)
            return "Error: LLM failed"

        # 🔥 SAFE UTF-8 DECODE
        output = result.stdout.decode("utf-8", errors="ignore").strip()

        if not output:
            return "Error: Empty response"

        return output

    except subprocess.TimeoutExpired:
        return "Error: Timeout"

    except Exception as e:
        return f"Error: {str(e)}"