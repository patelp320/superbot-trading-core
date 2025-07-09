import csv
import datetime
import os


def annotate_trade(ticker, strategy, confidence, signals):
    """Annotate why a trade was selected and log the explanation."""
    reasons = []
    if confidence > 0.7:
        reasons.append("High multi-agent confidence")
    if "oversold" in signals:
        reasons.append("RSI indicates oversold condition")
    if "news_positive" in signals:
        reasons.append("Recent news sentiment is positive")
    if "iv_high" in signals:
        reasons.append("Implied volatility favorable for premium selling")

    explanation = f"{strategy} triggered due to: " + ", ".join(reasons)
    print(f"[ANNOTATOR] {ticker} → {explanation}")

    os.makedirs("logs", exist_ok=True)
    with open("logs/annotation_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().isoformat(), ticker, strategy, confidence, explanation])
    return explanation
