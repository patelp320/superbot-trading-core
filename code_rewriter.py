import os
import shutil


def fix_module_from_log(log_file):
    with open(log_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        if "Traceback" in line or "line" in line:
            print(f"[REWRITER] 🔧 Found crash: {line.strip()}")
            break

    broken_module = "example_module.py"  # Extract from traceback dynamically
    fix_path = f"templates/{broken_module}"
    dest_path = f"modules/fixed/{broken_module}"

    if os.path.exists(fix_path):
        shutil.copy(fix_path, dest_path)
        print(f"[REWRITER] ✅ Rewrote {broken_module} to fixed version.")
    else:
        print("⚠️ No known fix found.")
