import React from "react";
import { Footer } from "../components/Footer.jsx";
import { loginWithSpotify } from "../services/auth_api.js";

export default function Home() {
  return (
    <div className="home container">
      <div className="hero">
        <img src="assets/images/logo.png" alt="SpotR Logo" className="logo" />
        <br></br>
        <h2>Your music, Your Mood, Unveiled</h2>
        <button
          className="cta-button"
          onClick={() => {
           loginWithSpotify();
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
