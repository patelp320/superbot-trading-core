import schedule
import time
import subprocess
import os
from datetime import datetime, timedelta, time as dt_time

log_dir = "../logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "learn.log")

def log(msg):
    timestamp = datetime.utcnow().isoformat()
    full = f"[{timestamp}] {msg}"
    print(full)
    with open(log_file, "a") as f:
        f.write(full + "\n")

def learn(max_tickers="100"):
    """Train models and generate the penny watchlist."""
    log("🧠 Running learn_core.py...")
    env = os.environ.copy()
    env.setdefault("MAX_SCAN_TICKERS", str(max_tickers))
    subprocess.call(["python3", "learn_core.py"], env=env)

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

def execute_trades():
    log("💸 Executing trades with ibkr_executor_sim.py")
    subprocess.call(["python3", "ibkr_executor_sim.py"])

def in_market_hours():
    now = datetime.utcnow() - timedelta(hours=4)
    return dt_time(9, 30) <= now.time() <= dt_time(16, 0)

def run_penny():
    if in_market_hours():
        log("🪙 Running penny_ai.py...")
        subprocess.call(["python3", "penny_ai.py"])

def run_options_update():
    log("🎯 Running options_ai.py updates...")
    subprocess.call(["python3", "options_ai.py"])


def run_sequence():
    """Run core modules once in a logical order."""
    # Limit the initial scan so the pipeline completes quickly
    learn(max_tickers="50")
    run_penny()
    predict()
    run_options_update()
    grade()
    evolve()
    report()
    execute_trades()
    repair()



schedule.every(10).minutes.do(learn)
schedule.every().hour.do(repair)
schedule.every(30).minutes.do(run_penny)
schedule.every(15).minutes.do(lambda: predict() if in_market_hours() else None)
schedule.every().day.at("15:45").do(run_options_update)
schedule.every().day.at("16:30").do(run_options_update)
schedule.every().day.at("16:30").do(predict)
schedule.every().day.at("17:00").do(grade)
schedule.every().day.at("09:35").do(execute_trades)
schedule.every().day.at("15:59").do(execute_trades)
schedule.every(3).hours.do(evolve)
schedule.every(3).hours.do(report)
schedule.every().hour.do(lambda: subprocess.call(["python3", "ai_modules/news_sentiment_ai.py"]))
schedule.every().day.at("07:00").do(lambda: subprocess.call(["python3", "ai_modules/macro_trend_ai.py"]))
schedule.every().day.at("17:30").do(lambda: subprocess.call(["python3", "strategy_engine/superbacktester.py"]))
schedule.every().day.at("02:00").do(lambda: subprocess.call(["python3", "strategy_engine/self_optimizer_ai.py"]))
schedule.every().day.at("08:45").do(lambda: subprocess.call(["python3", "penny_scanner_ai.py"]))
schedule.every().day.at("09:35").do(lambda: subprocess.call(["python3", "penny_ai.py"]))
schedule.every().day.at("16:15").do(lambda: subprocess.call(["python3", "learn_core.py"]))
schedule.every().day.at("17:00").do(lambda: subprocess.call(["python3", "email_reporter.py"]))

if __name__ == "__main__":
    run_sequence()
    log("🔄 Entering scheduler loop")
    schedule.run_pending()
    while True:
        schedule.run_pending()
        time.sleep(10)
