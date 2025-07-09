import json


def get_broker():
    with open("config.json") as f:
        config = json.load(f)

    mode = config.get("mode", "paper")
    if mode == "live":
        print("🚨 LIVE MODE ENABLED")
        from ibkr_executor_live import Broker
    else:
        print("🧪 Paper mode enabled")
        from ibkr_executor_sim import Broker

    return Broker()
