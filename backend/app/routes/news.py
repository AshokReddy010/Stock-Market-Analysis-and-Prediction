from fastapi import APIRouter, Query
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

@router.get("/news")
def get_stock_news(ticker: str = Query(..., description="Stock ticker like AAPL, TSLA, INFY")):
    try:
        params = {
            "q": ticker,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": NEWS_API_KEY,
            "pageSize": 5
        }
        response = requests.get(NEWS_ENDPOINT, params=params)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            return {"error": data.get("message", "Failed to fetch news")}

        articles = [{
            "title": a["title"],
            "description": a["description"],
            "url": a["url"],
            "published_at": a["publishedAt"]
        } for a in data["articles"]]

        return {
            "ticker": ticker.upper(),
            "articles": articles
        }

    except Exception as e:
        return {"error": str(e)}
