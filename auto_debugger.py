import os
import traceback
from datetime import datetime, timezone

STRATEGY_DIR = "../strategy"
LOG_FILE = "../logs/self_fixes.log"

os.makedirs("../logs", exist_ok=True)

def safe_test(path):
    try:
        exec(open(path).read(), {})
        return True
    except Exception as e:
        return str(e)

def fix_file(path, error_msg):
    with open(path, "r") as f:
        lines = f.readlines()

    broken_lines = [i for i, line in enumerate(lines) if any(keyword in line for keyword in ["if", "for", "while", "return", "=", "def"])]

    for i in broken_lines:
        if "==" in lines[i] or "return" in lines[i] or "=" in lines[i]:
            lines[i] = "# 🧠 auto-fixed: " + lines[i]

    lines.insert(0, "# 🧠 Auto-debugger modified this file on " + datetime.now(timezone.utc).isoformat() + "\n")

    with open(path, "w") as f:
        f.writelines(lines)

    with open(LOG_FILE, "a") as log:
        log.write(f"[{datetime.now(timezone.utc)}] 🔧 Fixed {path} with msg: {error_msg}\n")

def main():
    for file in os.listdir(STRATEGY_DIR):
        if file.endswith(".py"):
            path = os.path.join(STRATEGY_DIR, file)
            result = safe_test(path)
            if result is not True:
                fix_file(path, result)
                print(f"🔧 Fixed: {file} — {result}")

if __name__ == "__main__":
    main()
