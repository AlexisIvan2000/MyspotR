import React from "react";
import { useNavigate } from "react-router-dom";
import { Footer } from "../components/Footer";

export default function Home() {
  const navigate = useNavigate();
  const handleLogin = () => {
    navigate("/dashboard");
  };
  return (
    <div className="home container">
      <div className="hero">
        <img src="assets/images/logo.png" alt="SpotR Logo" className="logo" />
        <br></br>
        <h2>Your music, Your Mood, Unveiled</h2>
        <button
          className="cta-button"
          onClick={() => {
            handleLogin();
          }}
        >
          Continue with Spotify
        </button>
        <p className="subtext">
          We analyze your recently tracks to determine your musical mood.
        </p>
      </div>
      <Footer />          
    </div>
  );
}
