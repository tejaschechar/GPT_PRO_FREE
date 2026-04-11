import subprocess
import tempfile
import os
import sys


def run_python_code(code: str, timeout: int = 5):
    file_path = None

    try:
        # 🧾 Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode("utf-8"))
            file_path = f.name

        # 🚀 Run in isolated mode
        result = subprocess.run(
            [sys.executable, "-I", file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        # ✂️ Safety trimming
        output = output[-2000:] if output else ""
        error = error[-2000:] if error else ""

        return {
            "output": output,
            "error": error
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "",
            "error": "Execution timed out"
        }

    except Exception as e:
        return {
            "output": "",
            "error": str(e)
        }

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass