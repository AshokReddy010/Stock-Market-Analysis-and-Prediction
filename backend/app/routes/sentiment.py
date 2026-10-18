from fastapi import APIRouter
from textblob import TextBlob  # type: ignore

from app.routes.news import get_stock_news

router = APIRouter()


def score_headlines(titles: list[str]) -> dict:
    """Count headlines as positive (polarity > 0.1), negative (< -0.1) or neutral."""
    pos = neu = neg = 0
    for title in titles:
        if not title:
            continue
        polarity = TextBlob(title).sentiment.polarity
        if polarity > 0.1:
            pos += 1
        elif polarity < -0.1:
            neg += 1
        else:
            neu += 1
    overall = "Positive" if pos > neg else "Negative" if neg > pos else "Neutral"
    return {"positive": pos, "neutral": neu, "negative": neg, "overall": overall}


@router.get("/sentiment/{symbol}")
def analyze_sentiment(symbol: str):
    news = get_stock_news(ticker=symbol)  # a direct call, not an HTTP request back to this server
    return score_headlines([a.get("title", "") for a in news.get("articles", [])])
