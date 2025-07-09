"""
Displays pre-trade candidates and their estimated win rate for review.
"""

def preview_trades(trade_candidates):
    """Prints the top three trade candidates sorted by confidence."""
    print("\U0001F4CB Trade Preview:")
    for i, trade in enumerate(sorted(trade_candidates, key=lambda t: t.get('confidence', 0), reverse=True)[:3]):
        print(f"{i+1}. {trade['symbol']} | Win chance: {trade['confidence']:.1%} | Reason: {trade['reason']}")
