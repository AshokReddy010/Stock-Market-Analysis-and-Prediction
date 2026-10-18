from fastapi import APIRouter

from app.routes.sentiment import analyze_sentiment
from app.services.predictions import get_real_predictions

router = APIRouter()


def decide(trend_change: float, sentiment_score: int) -> str:
    """BUY when the forecast rises and positive headlines outnumber negative ones, SELL when both point down."""
    if trend_change > 0 and sentiment_score > 0:
        return "BUY"
    if trend_change < 0 and sentiment_score < 0:
        return "SELL"
    return "HOLD"


@router.get("/recommendation/{symbol}")
def get_recommendation(symbol: str):
    try:
        predictions = get_real_predictions(symbol.upper())
        sentiment = analyze_sentiment(symbol)
    except Exception as e:  # upstream data errors are reported, not raised
        return {"error": str(e)}
    linear = predictions.get("linear", [])
    if len(linear) < 2:
        return {"error": "Not enough prediction data"}
    trend_change = linear[-1]["predicted"] - linear[0]["predicted"]
    sentiment_score = sentiment["positive"] - sentiment["negative"]
    return {
        "symbol": symbol.upper(),
        "recommendation": decide(trend_change, sentiment_score),
        "trend_change": round(trend_change, 2),
        "sentiment_score": sentiment_score,
        "model_used": "Linear Regression + News Sentiment",
        "disclaimer": "Educational project, not investment advice.",
    }
