import os

ALLOWED_EXTENSIONS = {".txt", ".md", ".py", ".json", ".log", ".csv"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# 🔒 PROJECT ROOT SAFETY (IMPORTANT)
BASE_DIR = os.path.abspath(os.getcwd())


def read_file(file_path: str, max_chars: int = 5000):

    try:
        # 🔒 Resolve absolute path
        abs_path = os.path.abspath(file_path)

        # 🔒 BLOCK PATH TRAVERSAL
        if not abs_path.startswith(BASE_DIR):
            return "Blocked: Access outside project directory"

        if not os.path.exists(abs_path):
            return "File not found"

        _, ext = os.path.splitext(abs_path)

        if ext not in ALLOWED_EXTENSIONS:
            return f"Blocked file type: {ext}"

        if os.path.getsize(abs_path) > MAX_FILE_SIZE:
            return "File too large to read safely"

        with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)

        # ✂️ Smart trimming (important for LLM context)
        if len(content) > max_chars:
            content = content[:max_chars] + "\n...TRUNCATED"

        return content

    except Exception as e:
        return f"Error reading file: {str(e)}"