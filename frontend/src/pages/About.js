// src/pages/About.jsx
import React from 'react';
import './About.css';
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function About() {
  return (
    <div className="about-container">
      <header className="navbar">
        <img src={logo} alt="App Logo" className="logo" />
        <nav>
          <Link to="/dashboard">Home</Link>
          <Link to="/currency-converter">Currency Converter</Link>
          <Link to="/about">About</Link>
        </nav>
      </header>

      <main className="about-content">
        <h1>About This Application</h1>
        <p>
          This web application leverages real-time stock market data and machine learning algorithms to predict stock prices for the next 7 days. It combines financial news sentiment with ARIMA, LSTM, and Linear Regression models to help users make informed decisions.
        </p>
        <p>
          Users can register, log in, track stocks, get predictions, read financial news, and convert currencies. Admins can manage users and send email alerts.
        </p>
        <p>
          Built with <strong>FastAPI</strong>, <strong>React</strong>, and <strong>Machine Learning</strong>.
        </p>
      </main>
    </div>
  );
}
