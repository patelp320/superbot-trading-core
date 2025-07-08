import schedule
import time
import subprocess
import os
from datetime import datetime

log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "learn.log")

def log(msg):
    timestamp = datetime.utcnow().isoformat()
    full = f"[{timestamp}] {msg}"
    print(full)
    with open(log_file, "a") as f:
        f.write(full + "\n")

def learn():
    log("🧠 Running learn_core.py...")
    subprocess.call(["python3", "learn_core.py"])

def predict():
    log("🔮 Running predict_core.py...")
    subprocess.call(["python3", "predict_core.py"])

def report():
    log("📧 Running email_reporter.py...")
    subprocess.call(["python3", "email_reporter.py"])

def grade():
    log("🧪 Running strategy_grader.py...")
    subprocess.call(["python3", "strategy_grader.py"])

def evolve():
    log("🧠 Generating new strategies...")
    subprocess.call(["python3", "strategy_writer.py"])

def repair():
    log("🔧 Running self_runner + auto_debugger...")
    subprocess.call(["python3", "self_runner.py"])

def main():
    log("✅ Scheduler started")
    learn()

    schedule.every(10).minutes.do(learn)
    schedule.every().hour.do(repair)
    schedule.every().day.at("16:30").do(predict)
    schedule.every().day.at("17:00").do(grade)
    schedule.every(3).hours.do(evolve)
    schedule.every(3).hours.do(report)

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
