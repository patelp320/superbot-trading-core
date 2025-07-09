def is_pump(price_change, has_news):
    return price_change > 1.5 and not has_news
