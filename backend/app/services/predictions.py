"""Seven-day price forecasts from three models, each with an honest out-of-sample check.

Earlier versions reported in-sample R² as "accuracy". On a price series that is close to 99% for any model,
because tomorrow's price is near today's, so it says nothing. Each model is now also refit without the last
7 trading days and scored on how well it forecasts them (mean absolute percentage error), next to the naive
forecast "the price stays where it is". A model is only useful if it beats that baseline.
"""

import datetime

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA

HORIZON = 7


def mape(actual, predicted) -> float:
    actual, predicted = np.asarray(actual, dtype=float), np.asarray(predicted, dtype=float)
    return float(np.mean(np.abs((actual - predicted) / actual)) * 100)


def predict_linear(data, horizon=HORIZON):
    df = pd.DataFrame({"Close": data})
    df["Lag1"] = df["Close"].shift(1)
    df["Lag2"] = df["Close"].shift(2)
    df["RollingMean5"] = df["Close"].rolling(window=5).mean()
    df = df.dropna()
    x_cols = ["Lag1", "Lag2", "RollingMean5"]
    model = LinearRegression().fit(df[x_cols], df["Close"])
    fit = r2_score(df["Close"], model.predict(df[x_cols]))
    history = list(data[-5:])
    preds = []
    for _ in range(horizon):
        row = pd.DataFrame([[history[-1], history[-2], float(np.mean(history[-5:]))]], columns=x_cols)
        nxt = float(model.predict(row)[0])
        preds.append(nxt)
        history.append(nxt)
    return preds, fit


def predict_arima(data, horizon=HORIZON):
    model_fit = ARIMA(np.asarray(data, dtype=float), order=(5, 1, 0)).fit()
    preds = model_fit.forecast(steps=horizon)
    return [float(p) for p in preds], r2_score(data, model_fit.fittedvalues)


def predict_lstm(data, horizon=HORIZON, epochs=5):
    """Two-layer LSTM on 30-day windows. Needs TensorFlow; returns None when it is not installed."""
    try:
        from keras.layers import LSTM, Dense
        from keras.models import Sequential
    except ImportError:
        return None, None
    series = np.asarray(data, dtype=float).reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(series).flatten()
    window = 30
    x = np.array([scaled[i - window:i] for i in range(window, len(scaled))])[..., None]
    y = scaled[window:]
    model = Sequential([LSTM(50, return_sequences=True, input_shape=(window, 1)), LSTM(50), Dense(1)])
    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(x, y, epochs=epochs, batch_size=32, verbose=0)
    seq = scaled[-window:].tolist()
    preds = []
    for _ in range(horizon):
        nxt = float(model.predict(np.array(seq[-window:])[None, :, None], verbose=0)[0][0])
        preds.append(nxt)
        seq.append(nxt)
    fit = r2_score(y, model.predict(x, verbose=0).flatten())
    return scaler.inverse_transform(np.array(preds).reshape(-1, 1)).flatten().tolist(), fit


MODELS = {"linear": predict_linear, "arima": predict_arima, "lstm": predict_lstm}


def backtest(data, horizon=HORIZON) -> dict:
    """Refit each model without the last `horizon` days and measure its error on them."""
    train, test = data[:-horizon], data[-horizon:]
    out = {"naive_mape": round(mape(test, [train[-1]] * horizon), 2)}
    for name, fn in MODELS.items():
        preds, _ = fn(train, horizon)
        out[f"{name}_mape"] = None if preds is None else round(mape(test, preds), 2)
    return out


def forecast(close_prices, base_date=None) -> dict:
    data = np.asarray(close_prices, dtype=float)
    data = data[~np.isnan(data)]
    if len(data) < 60:
        raise ValueError("need at least 60 days of prices")
    base_date = base_date or datetime.date.today()
    dates = [(base_date + datetime.timedelta(days=i)).isoformat() for i in range(1, HORIZON + 1)]
    result: dict = {}
    for name, fn in MODELS.items():
        preds, fit = fn(data)
        result[name] = [] if preds is None else [{"date": d, "predicted": round(float(p), 2)} for d, p in zip(dates, preds, strict=False)]
        result[f"{name}_accuracy"] = None if fit is None else round(float(fit) * 100, 2)  # in-sample R², kept for the UI
    result["backtest"] = backtest(data)
    return result


def get_real_predictions(symbol="AAPL"):
    hist = yf.Ticker(symbol).history(period="5y")
    if hist.empty:
        raise ValueError(f"no price history for {symbol}")
    return {"symbol": symbol.upper(), **forecast(hist["Close"].values)}
