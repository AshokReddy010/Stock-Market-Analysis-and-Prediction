# routes/sentiment.py
from fastapi import APIRouter
from textblob import TextBlob
from .tweets import get_stock_tweets

router = APIRouter()

@router.get("/sentiment/{symbol}")
def analyze_sentiment(symbol: str):
    tweet_response = get_stock_tweets(symbol)
    tweets = tweet_response["tweets"]

    pos, neu, neg = 0, 0, 0

    for tweet in tweets:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0.1:
            pos += 1
        elif polarity < -0.1:
            neg += 1
        else:
            neu += 1

    overall = "Positive" if pos > neg else "Negative" if neg > pos else "Neutral"
    return {
        "positive": pos,
        "neutral": neu,
        "negative": neg,
        "overall": overall
    }
