import React, { useEffect } from "react";
import "./Home.css";
import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const Home = () => {
  // ✅ Automatically logout user when they visit Home
  useEffect(() => {
    localStorage.removeItem("token");
  }, []);

  const token = localStorage.getItem("token");

  return (
    <div className="home-container">
      <header className="navbar">
        <img src={logo} alt="ADFG Logo" className="logo" />
        <div className="nav-links">
          <nav>
            <Link to={token ? "/dashboard" : "/"}>Home</Link>
            <Link to="/about">About</Link>
            <Link to="/currency-converter">Currency Converter</Link>
            <Link to="/contact">Contact Us</Link>
          </nav>
          <div className="auth-buttons">
            <Link to="/login" className="login-btn">Login</Link>
            <Link to="/register" className="register-btn">Register</Link>
          </div>
        </div>
      </header>

      <section className="hero">
        <div className="hero-overlay">
          <h1>STOCK MARKET PREDICTION</h1>
          <p>WELCOME TO THE FUTURE OF INVESTING!</p>
        </div>
      </section>

      <section className="stats-section">
        <div className="stat"><h2>3</h2><p>Forecasting Models</p></div>
        <div className="stat"><h2>7 Days</h2><p>Forecast Horizon</p></div>
        <div className="stat"><h2>2</h2><p>Markets: NASDAQ and NSE</p></div>
      </section>

      <section className="services-section">
        <h2>WHAT IT DOES</h2>
        <div className="services">
          <div>🕒 Live Stock Prices</div>
          <div>📈 7-Day Price Forecasts</div>
          <div>📰 News Sentiment Analysis</div>
          <div>✅ Buy, Sell or Hold Signal</div>
          <div>💱 Currency Converter</div>
          <div>🔒 Secure Sign-In</div>
        </div>
      </section>

      <section className="contact-section">
        <div className="contact-info">
          <h2>GET IN TOUCH WITH US</h2>
          <form>
            <input type="text" placeholder="First Name" />
            <input type="text" placeholder="Last Name" />
            <input type="email" placeholder="Your Email" />
            <textarea placeholder="Message" />
            <button type="submit">SEND MESSAGE</button>
          </form>
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2025 ADFG. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
