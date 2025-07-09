import os

AI_MODULES_DIR = "ai_modules"

def auto_add_docstrings(ai_modules_path: str = AI_MODULES_DIR) -> None:
    """Insert placeholder docstrings at the top of modules if missing."""
    for file in os.listdir(ai_modules_path):
        if file.endswith(".py"):
            full_path = os.path.join(ai_modules_path, file)
            with open(full_path, "r") as f:
                lines = f.readlines()

            if not lines:
                continue

            # Skip empty __init__.py
            if file == "__init__.py" and len(lines) == 1 and lines[0].strip() == "":
                continue

            # Check for existing docstring
            first_line = lines[0].strip()
            if first_line.startswith('"""') or first_line.startswith("'''"):
                continue

            docstring = f'"""TODO: Add module description for {file.replace(".py", "")}."""\n\n'
            new_content = [docstring] + lines
            with open(full_path, "w") as f:
                f.writelines(new_content)
            print(f"\u2705 Docstring added to {file}")

if __name__ == "__main__":
    auto_add_docstrings()
