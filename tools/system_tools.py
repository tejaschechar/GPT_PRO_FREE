import subprocess
import shlex
import os

ALLOWED_COMMANDS = {
    "ls",
    "pwd",
    "echo",
    "whoami",
    "date",
    "cat"
}

MAX_OUTPUT = 2000


def run_system_command(command: str):
    try:
        parts = shlex.split(command)

        if not parts:
            return {"error": "Empty command"}

        base_cmd = parts[0]

        # 🔒 ALLOWLIST CHECK
        if base_cmd not in ALLOWED_COMMANDS:
            return {"error": f"Command not allowed: {base_cmd}"}

        # 🔒 BASIC SAFETY BLOCKS
        for arg in parts:
            if ".." in arg or "/" in arg and base_cmd == "cat":
                return {"error": "Path traversal blocked"}

        result = subprocess.run(
            parts,
            shell=False,
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()[-MAX_OUTPUT:]
        error = result.stderr.strip()[-MAX_OUTPUT:]

        return {
            "output": output,
            "error": error
        }

    except subprocess.TimeoutExpired:
        return {"error": "Command timed out"}

    except Exception as e:
        return {"error": str(e)}