"""Settings from environment variables, so no secret lives in the code.

    JWT_SECRET      signing key for login tokens (required when APP_ENV=production)
    DATABASE_URL    SQLAlchemy URL, default: SQLite file next to the app
    CORS_ORIGINS    comma-separated front-end origins, default: http://localhost:3000
    NEWS_API_KEY    newsapi.org key for headlines (optional; sentiment is skipped without it)
"""

import logging
import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger("stockapp")

APP_ENV = os.getenv("APP_ENV", "development")
JWT_SECRET = os.getenv("JWT_SECRET", "")
if not JWT_SECRET:
    if APP_ENV == "production":
        raise RuntimeError("JWT_SECRET must be set in production")
    JWT_SECRET = secrets.token_hex(32)  # development: a fresh key per process, so tokens never outlive a restart
    log.warning("JWT_SECRET is not set; using a temporary development key")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{Path(__file__).resolve().parent / 'stockapp.db'}")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
