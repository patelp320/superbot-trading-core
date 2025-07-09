import random
from datetime import datetime, timezone

REGIMES = ["BULL", "BEAR", "CHOP"]


def detect_regime() -> str:
    return random.choice(REGIMES)


def main():
    regime = detect_regime()
    with open("../data/macro_regime.txt", "w") as f:
        f.write(regime)
    print(f"[{datetime.now(timezone.utc)}] 🌎 Market regime -> {regime}")


def current_regime() -> str:
    try:
        with open("../data/macro_regime.txt", "r") as f:
            return f.read().strip()
    except Exception:
        return "UNKNOWN"


if __name__ == "__main__":
    main()
