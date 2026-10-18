from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware  # type: ignore

from app.config import CORS_ORIGINS
from app.database import Base, engine
from app.models import user as user_model  # noqa: F401 - registers the table before create_all
from app.routes import (
    admin,
    auth,
    currency,
    history,
    news,
    predictions,
    recommendation,
    sentiment,
    stock,
    tweets,
    user,
    user_admin,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Market Analysis and Prediction API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(user_admin.router, prefix="/api/admin/users", tags=["User Management"])
app.include_router(stock.router, prefix="/api/stock", tags=["Stock Data"])
app.include_router(news.router, prefix="/api", tags=["News"])
app.include_router(currency.router, prefix="/api/currency", tags=["Currency Converter"])
app.include_router(tweets.router, prefix="/api")
app.include_router(sentiment.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(history.router, prefix="/api", tags=["History"])
app.include_router(recommendation.router, prefix="/api", tags=["Recommendation"])
