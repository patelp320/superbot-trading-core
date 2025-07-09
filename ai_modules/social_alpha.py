import json
import re
import requests
from datetime import datetime, timezone

HEADERS = {"User-Agent": "superbot"}


def fetch_wallstreetbets(limit: int = 20) -> list[str]:
    url = f"https://www.reddit.com/r/wallstreetbets/new.json?limit={limit}"
    tickers = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        if r.ok:
            posts = r.json().get("data", {}).get("children", [])
            for p in posts:
                text = p.get("data", {}).get("title", "")
                tickers += re.findall(r"\b[A-Z]{3,5}\b", text)
    except Exception:
        pass
    return tickers


def fetch_stocktwits(symbol: str = "SPY") -> list[str]:
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    tickers = []
    try:
        r = requests.get(url, timeout=5)
        if r.ok:
            messages = r.json().get("messages", [])
            for m in messages:
                body = m.get("body", "")
                tickers += re.findall(r"\$([A-Z]{2,5})", body)
    except Exception:
        pass
    return tickers


def aggregate_trending() -> list[tuple[str, int]]:
    seen = fetch_wallstreetbets() + fetch_stocktwits()
    counts: dict[str, int] = {}
    for t in seen:
        t = t.upper()
        counts[t] = counts.get(t, 0) + 1
    trending = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]
    path = "../data/social_alpha.json"
    with open(path, "w") as f:
        json.dump({"timestamp": datetime.now(timezone.utc).isoformat(), "trending": trending}, f)
    print(f"[{datetime.now(timezone.utc)}] \U0001F4AC Social alpha saved -> {path}")
    return trending


def load_social_alpha() -> dict:
    try:
        with open("../data/social_alpha.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    aggregate_trending()
