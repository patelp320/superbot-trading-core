"""Track strategy versions and hashes."""
import csv
import hashlib
import os
import time


def hash_file(path: str) -> str:
    """Return md5 hash of file contents."""
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def audit_strategies() -> None:
    """Log hashes of all alpha strategy files."""
    log_path = "logs/strategy_audit_log.csv"
    seen = set()

    if os.path.exists(log_path):
        with open(log_path) as f:
            for line in f:
                seen.add(line.split(",")[0])

    os.makedirs("logs", exist_ok=True)
    with open(log_path, "a", newline="") as f:
        writer = csv.writer(f)
        for file in os.listdir("strategies"):
            if file.startswith("alpha_") and file.endswith(".py"):
                path = f"strategies/{file}"
                sig = hash_file(path)
                if sig not in seen:
                    writer.writerow([sig, file, int(time.time())])
                    print(f"[AUDIT] Logged new strategy version: {file}")


if __name__ == "__main__":  # pragma: no cover - manual trigger
    audit_strategies()
