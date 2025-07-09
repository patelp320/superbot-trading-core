from agent_tech import vote as tech_vote
from agent_macro import vote as macro_vote
from agent_news import vote as news_vote
from agent_volatility import vote as vol_vote


def ensemble_vote(ticker):
    votes = [
        tech_vote(ticker),
        macro_vote(ticker),
        news_vote(ticker),
        vol_vote(ticker)
    ]
    avg_conf = sum(votes) / len(votes)

    if avg_conf > 0.65:
        decision = "BUY"
    elif avg_conf < 0.35:
        decision = "SELL"
    else:
        decision = "HOLD"

    print(f"[AGENTS] {ticker} — Avg Confidence: {avg_conf:.2f} → {decision}")
    return avg_conf, decision
