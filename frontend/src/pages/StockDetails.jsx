import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import "./StockDetails.css";
import logo from "../assets/logo.png";

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from "recharts";

const COLORS = ["#00ff99", "#8884d8", "#ff4d4d"];
const RANGES = ["5d", "1mo", "1y", "5y", "max"];
const RANGE_LABELS = {
  "5d": "1 Week",
  "1mo": "1 Month",
  "1y": "1 Year",
  "5y": "5 Year",
  "max": "All Time"
};

const StockDetails = () => {
  const { symbol } = useParams();
  const [details, setDetails] = useState({});
  const [predictions, setPredictions] = useState({});
  const [tweets, setTweets] = useState([]);
  const [sentiment, setSentiment] = useState({});
  const [range, setRange] = useState("1mo");
  const [trendData, setTrendData] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAll = async () => {
    setLoading(true);
    try {
      const [
        detailRes,
        predictionRes,
        tweetRes,
        sentimentRes,
        historyRes
      ] = await Promise.all([
        axios.get(`http://localhost:8000/api/stock/details?tickers=${symbol}`),
        axios.get(`http://localhost:8000/api/predictions/${symbol}`),
        axios.get(`http://localhost:8000/api/tweets/${symbol}`),
        axios.get(`http://localhost:8000/api/sentiment/${symbol}`),
        axios.get(`http://localhost:8000/api/stock/history/${symbol}?range=${range}`)
      ]);

      setDetails(detailRes.data[0]);
      setPredictions(predictionRes.data);
      setTweets(tweetRes.data.tweets || []);
      setSentiment(sentimentRes.data);
      setTrendData(historyRes.data.history || []);
    } catch (err) {
      console.error("❌ Failed to load stock details:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAll();
  }, [symbol, range]);

  return (
    <div className="stock-details-container">
      <header className="navbar">
        <img src={logo} alt="ADFG Logo" className="logo" />
        <nav>
          <Link to="/dashboard">Home</Link>
          <Link to="/currency-converter">Currency Converter</Link>
          <Link to="/contact">Contact Us</Link>
        </nav>
      </header>

      <h2 className="details-title">{symbol.toUpperCase()} — Full Stock Analysis</h2>

      {loading ? (
        <p className="loading">Loading data...</p>
      ) : (
        <>
          {/* Snapshot Cards */}
          <div className="snapshot-cards">
            <div className="snap">Value<br /><strong>${details.price}</strong></div>
            <div className={`snap ${details.change >= 0 ? "green" : "red"}`}>Change<br /><strong>{details.change}</strong></div>
            <div className={`snap ${details.percent_change >= 0 ? "green" : "red"}`}>% Change<br /><strong>{details.percent_change}%</strong></div>
            <div className="snap">Open<br /><strong>${details.open}</strong></div>
            <div className="snap">High<br /><strong>${details.high}</strong></div>
            <div className="snap">Low<br /><strong>${details.low}</strong></div>
            <div className="snap">Prev Close<br /><strong>${details.previous_close}</strong></div>
          </div>

          {/* Trend Chart */}
          <div className="card">
            <div className="range-buttons">
              {RANGES.map(r => (
                <button
                  key={r}
                  onClick={() => setRange(r)}
                  className={range === r ? "active" : ""}
                >
                  {RANGE_LABELS[r]}
                </button>
              ))}
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={trendData}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <CartesianGrid strokeDasharray="3 3" />
                <Line type="monotone" dataKey="close" stroke="#ffa500" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Predictions */}
          <div className="prediction-section">
            {["arima", "lstm", "linear"].map((model) => (
              <div className="prediction-card" key={model}>
                <h3>{model.toUpperCase()} Prediction</h3>
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart data={predictions[model]}>
                    <XAxis dataKey="date" interval={0} angle={-45} textAnchor="end" height={60} />
                    <YAxis />
                    <Tooltip />
                    <CartesianGrid strokeDasharray="3 3" />
                    <Line type="monotone" dataKey="predicted" stroke="#00ff99" dot={{ r: 2 }} />
                  </LineChart>
                </ResponsiveContainer>
                <p className="rmse">RMSE: {predictions[`${model}_rmse`]}</p>
              </div>
            ))}
          </div>


          {/* Sentiment */}
          <div className="card">
            <h3>Sentiment Analysis</h3>
            <PieChart width={300} height={250}>
              <Pie
                data={[
                  { name: "Positive", value: sentiment.positive },
                  { name: "Neutral", value: sentiment.neutral },
                  { name: "Negative", value: sentiment.negative }
                ]}
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
                dataKey="value"
              >
                {COLORS.map((color, idx) => (
                  <Cell key={idx} fill={color} />
                ))}
              </Pie>
              <Legend />
            </PieChart>
            <p className={`overall ${sentiment.overall?.toLowerCase()}`}>
              Overall Sentiment: {sentiment.overall}
            </p>
          </div>

          {/* Tweets */}
          <div className="card">
            <h3>Recent Tweets</h3>
            <ul className="tweets">
              {tweets.map((t, i) => (
                <li key={i}>• {t}</li>
              ))}
            </ul>
          </div>

          {/* Final Recommendation */}
          <div className="card recommendation">
            <h3>📢 Recommendation</h3>
            <p>
              Based on current trends, prediction models, and sentiment analysis, our AI
              suggests: <strong className={sentiment.overall?.toLowerCase()}>{sentiment.overall}</strong>
            </p>
          </div>
        </>
      )}
    </div>
  );
};

export default StockDetails;
