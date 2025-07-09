"""
Detects penny stocks with momentum based on volume spikes, price action, and trend models.
"""


def detect_momentum_stocks(stock_data):
    result = []
    for stock in stock_data:
        if stock['price'] < 5 and stock['volume'] > stock['avg_volume'] * 3 and stock['trend'] > 0:
            result.append(stock)
    return sorted(result, key=lambda x: x['trend'], reverse=True)
