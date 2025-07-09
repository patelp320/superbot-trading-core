# hype_index.py
import random


def get_hype_score(ticker):
    reddit_mentions = random.randint(10, 500)
    twitter_mentions = random.randint(5, 300)

    hype = min(1.0, (reddit_mentions + twitter_mentions) / 1000)
    print(f"[HYPE] {ticker}: Reddit={reddit_mentions}, Twitter={twitter_mentions}, Score={hype}")
    return hype
