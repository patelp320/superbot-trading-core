import os
from datetime import datetime, timezone

grades_log = "../logs/strategy_grades.log"
results_dir = "../logs/results"
os.makedirs(results_dir, exist_ok=True)
os.makedirs("../logs", exist_ok=True)

def evaluate(filename):
    try:
        with open(os.path.join(results_dir, filename), "r") as f:
            lines = f.readlines()
        trades = [float(x.split("ROI:")[1]) for x in lines if "ROI:" in x]
        if len(trades) == 0:
            return 0.0
        avg_roi = sum(trades) / len(trades)
        win_rate = sum(1 for r in trades if r > 0) / len(trades)
        return round(avg_roi, 3), round(win_rate, 2)
    except:
        return 0.0, 0.0

with open(grades_log, "a") as log:
    for file in os.listdir(results_dir):
        if file.endswith(".txt"):
            avg_roi, win_rate = evaluate(file)
            status = "✅ PROMOTE" if avg_roi > 0.01 and win_rate > 0.6 else "❌ DEMOTE"
            msg = f"[{datetime.now(timezone.utc)}] {file}: ROI={avg_roi}, WinRate={win_rate} → {status}"
            print(msg)
            log.write(msg + "\n")
