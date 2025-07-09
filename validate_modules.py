import os
import importlib

MODULE_DIR = "ai_modules"


def validate_modules():
    print("\U0001F50D Validating placeholder modules...\n")
    for filename in os.listdir(MODULE_DIR):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                mod = importlib.import_module(f"{MODULE_DIR}.{module_name}")
                docstring = getattr(mod, "__doc__", "") or ""
                doc_check = bool(docstring.strip())
                func_check = any(
                    callable(getattr(mod, attr))
                    for attr in dir(mod)
                    if not attr.startswith("_")
                )

                print(f"\u2705 {module_name}: Imported successfully.")
                doc_status = "\u2714\ufe0f" if doc_check else "\u274c"
                func_status = "\u2714\ufe0f" if func_check else "\u274c"
                print(f"   {doc_status} Docstring present.")
                print(f"   {func_status} Callable functions found.\n")

            except Exception as e:
                print(f"\u274c Failed to import {module_name}: {e}\n")


if __name__ == "__main__":
    validate_modules()
