import json
import time
from adaptive_scheduler import decide_schedule
from auto_updater import run_update
from log_recovery import resume
from performance_tracker import summary
from alpha_discovery import discover_tickers
from real_mode_switch import get_broker


def load_config():
    with open("run_config.json", "r") as f:
        return json.load(f)


def run_cycle():
    decide_schedule()
    config = load_config()

    run_update()

    if config.get("run_penny_ai", True):
        import penny_ai
        penny_ai.run()

    if config.get("run_options_ai", True):
        import options_ai
        options_ai.run()

    import strategy_writer
    strategy_writer.run()

    resume()

    summary()


if __name__ == "__main__":
    print("🚀 Superbot Scheduler Starting...")
    discover_tickers()
    broker = get_broker()

    while True:
        run_cycle()
        print("🔁 Sleeping 30 min before next cycle...\n")
        time.sleep(1800)
