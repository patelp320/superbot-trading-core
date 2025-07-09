import json
import datetime
from macro_trend_ai import compute_macro_score


def decide_schedule():
    now = datetime.datetime.now()
    day = now.strftime("%A")
    hour = now.hour
    macro_score = compute_macro_score()

    config = {
        "run_penny_ai": day not in ["Friday"] and macro_score > 0.2,
        "run_options_ai": hour < 15,
        "run_strategy_writer": True,
        "run_news_sentiment": macro_score > 0
    }

    with open("run_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("[SCHEDULER] ✅ Decisions written:", config)
