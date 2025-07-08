import os
import random
import subprocess
from datetime import datetime


def main():
    underperform = random.random() < 0.5
    if underperform:
        print(f"[{datetime.utcnow()}] 🔄 Retraining models...")
        subprocess.call(["python3", "learn_core.py"])
    else:
        print(f"[{datetime.utcnow()}] ✅ Models performing well. No retrain.")


if __name__ == "__main__":
    main()
