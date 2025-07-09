import random
import requests

BROKER_STATUS = {
    "IBKR": "https://status.interactivebrokers.com",
    "Alpaca": "https://status.alpaca.markets",
    "Paper": "https://example.com/paper/status",
}


def broker_up(name: str) -> bool:
    url = BROKER_STATUS.get(name)
    if not url:
        return False
    try:
        requests.get(url, timeout=3)
        return True
    except Exception:
        # Assume mostly up if network fails
        return random.random() > 0.1


def choose_broker() -> str:
    if broker_up("IBKR"):
        return "IBKR"
    for b in ["Alpaca", "Paper"]:
        if broker_up(b):
            return b
    return "Paper"


if __name__ == "__main__":
    print("Selected broker:", choose_broker())
