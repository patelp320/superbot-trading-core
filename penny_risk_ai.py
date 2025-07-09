from datetime import datetime, timezone
import pandas as pd


def initial_stop(entry_price, vwap):
    return min(entry_price * 0.94, vwap)


def trail_stop(entry_price, current_price, atr):
    trailing = entry_price + 2 * atr
    return max(trailing, current_price * 0.92)


def manage_trade(df, entry_price):
    atr = df['Close'].tail(14).std() * 3
    vwap = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
    stop = initial_stop(entry_price, vwap.iloc[-1])
    target = entry_price * 1.2
    scale_price = entry_price * 1.08
    return {
        'stop': round(stop, 4),
        'trail': round(trail_stop(entry_price, df['Close'].iloc[-1], atr), 4),
        'target': round(target, 4),
        'scale': round(scale_price, 4),
    }

if __name__ == '__main__':
    print(f"[{datetime.now(timezone.utc)}] Penny risk manager ready.")
