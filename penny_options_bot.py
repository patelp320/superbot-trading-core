import os
from datetime import datetime, timezone

from options_ai import filter_candidate, sentiment as options_sentiment
from penny_ai import gap_up, high_short_interest, sentiment as penny_sentiment

WATCHLIST_FILE = "../logs/penny_watchlist.txt"
LOG_FILE = "../logs/penny_options.log"

os.makedirs("../logs", exist_ok=True)


def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return []
    with open(WATCHLIST_FILE) as f:
        return [line.strip() for line in f if line.strip()]


def evaluate(ticker):
    option_ok = filter_candidate(ticker)
    gap = gap_up(ticker)
    short_int = high_short_interest.get(ticker, 0)
    sentiment = (options_sentiment(ticker) + penny_sentiment(ticker)) / 2
    score = 0
    if option_ok:
        score += 1
    if gap > 0.05:
        score += 1
    if short_int > 0.25:
        score += 1
    if sentiment > 0.05:
        score += 1
    return score, option_ok, gap, short_int, sentiment


def main():
    candidates = []
    for ticker in load_watchlist():
        score, option_ok, gap, short_int, sentiment = evaluate(ticker)
        if score >= 2:
            msg = (
                f"[{datetime.now(timezone.utc)}] \U0001F4C8 {ticker} flagged | "
                f"score={score} | gap={round(gap*100,2)}% | short={short_int} | "
                f"sent={round(sentiment,2)}"
            )
            print(msg)
            candidates.append(msg)

    with open(LOG_FILE, "a") as log:
        for line in candidates:
            log.write(line + "\n")


if __name__ == "__main__":
    main()
