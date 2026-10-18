import numpy as np
import pytest

from app.routes import recommendation, sentiment
from app.services import predictions


def series(n=400, seed=0, drift=0.0005):
    rng = np.random.default_rng(seed)
    return 100 * np.exp(np.cumsum(rng.normal(drift, 0.01, n)))


def test_mape():
    assert predictions.mape([100, 200], [110, 180]) == pytest.approx(10.0)


def test_forecast_shape_and_backtest():
    out = predictions.forecast(series())
    assert len(out["linear"]) == 7 and len(out["arima"]) == 7
    bt = out["backtest"]
    assert {"naive_mape", "linear_mape", "arima_mape", "lstm_mape"} <= set(bt)
    assert bt["linear_mape"] < 10 and bt["naive_mape"] < 10        # a calm random walk: errors stay small


def test_lstm_is_skipped_without_tensorflow(monkeypatch):
    import builtins
    real = builtins.__import__

    def no_keras(name, *a, **k):
        if name.startswith("keras"):
            raise ImportError(name)
        return real(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", no_keras)
    out = predictions.forecast(series())
    assert out["lstm"] == [] and out["lstm_accuracy"] is None and out["backtest"]["lstm_mape"] is None


def test_too_little_history():
    with pytest.raises(ValueError):
        predictions.forecast(series(30))


@pytest.mark.parametrize("trend, senti, decision", [(1.0, 2, "BUY"), (-1.0, -1, "SELL"), (1.0, -1, "HOLD"), (0.0, 3, "HOLD")])
def test_decide(trend, senti, decision):
    assert recommendation.decide(trend, senti) == decision


def test_headline_scoring():
    s = sentiment.score_headlines(["Shares soar on excellent results", "Terrible losses hit the company", "Company holds meeting", ""])
    assert (s["positive"], s["negative"], s["neutral"], s["overall"]) == (1, 1, 1, "Neutral")


def test_recommendation_uses_functions_not_http(monkeypatch):
    monkeypatch.setattr(recommendation, "get_real_predictions",
                        lambda s: {"linear": [{"predicted": 100.0}, {"predicted": 104.0}]})
    monkeypatch.setattr(recommendation, "analyze_sentiment", lambda s: {"positive": 3, "negative": 1})
    r = recommendation.get_recommendation("aapl")
    assert r["recommendation"] == "BUY" and r["symbol"] == "AAPL" and r["trend_change"] == 4.0


def test_news_without_key_degrades(monkeypatch):
    from app.routes import news
    monkeypatch.setattr(news, "NEWS_API_KEY", "")
    assert news.get_stock_news(ticker="aapl")["articles"] == []
