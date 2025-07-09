"""Simple news sentiment scoring for tickers."""

from textblob import TextBlob


def get_headlines(ticker: str):
    """Return placeholder list of headlines for ``ticker``."""
    return [
        f"{ticker} launches new product line",
        f"{ticker} stock dips amid broader tech selloff",
        f"Analysts upgrade {ticker} price target",
    ]


def analyze_sentiment(ticker: str) -> float:
    """Compute average sentiment score for ``ticker`` headlines."""
    headlines = get_headlines(ticker)
    scores = [TextBlob(h).sentiment.polarity for h in headlines]
    avg_score = sum(scores) / len(scores)
    print(f"[SENTIMENT] {ticker}: {avg_score:.2f}")
    return avg_score


if __name__ == "__main__":  # pragma: no cover - example usage
    analyze_sentiment("AAPL")
