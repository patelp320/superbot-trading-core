"""TODO: Add module description for alt_data_ingest."""

import json
import requests
from datetime import datetime, timezone

# Placeholder API endpoints for various news and alternative data sources
SOURCES = {
    "Benzinga": "https://api.benzinga.com/api/v2/news",
    "UnusualWhales": "https://phx.unusualwhales.com/api/historic/news",
    "WhaleStream": "https://api.whalestream.com/v1/options/news",
    "FinBrain": "https://finbrain.tech/api/news",
}


def fetch_news() -> list[dict]:
    """Fetch news articles from multiple sources."""
    articles = []
    for name, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=5)
            data = r.json() if r.ok else {}
        except Exception:
            data = {}
        articles.append({"source": name, "data": data})
    return articles


def parse_filings(text: str) -> list[str]:
    """Extract key points from SEC filings or transcripts."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    summary = lines[:3]
    if not summary and text:
        summary = [text[:200]]
    return summary


def collect_alt_data() -> dict:
    news = fetch_news()
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "news": news}
    path = "../data/alt_data.json"
    with open(path, "w") as f:
        json.dump(payload, f)
    print(f"[{datetime.now(timezone.utc)}] 📵 Alt data saved -> {path}")
    return payload


def load_alt_data() -> dict:
    try:
        with open("../data/alt_data.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}


if __name__ == "__main__":
    collect_alt_data()
