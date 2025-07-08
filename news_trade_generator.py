from ai_modules.news_sentiment_ai import load_scores
from datetime import datetime

KEYWORDS = ["Acquisition", "FDA Approval"]


def generate_trades():
    scores = load_scores()
    for ticker, score in scores.items():
        if score > 0.5:
            print(f"[{datetime.utcnow()}] 📢 News trade: Buying {ticker} on positive news")


if __name__ == "__main__":
    generate_trades()
