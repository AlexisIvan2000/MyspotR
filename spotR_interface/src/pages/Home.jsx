import React from "react";

export default function Home() {
  return (
    <div className="home container">
      <div className="hero">
        <h1>SpotR</h1>
        <br></br>
        <h2>Your music, Your Mood, Unveiled</h2>
        <button className="cta-button" onClick={() => {}}>
          LOG IN WITH SPOTIFY
        </button>
        <p className="subtext">
          We analyze your recently tracks to determine your musical mood.
        </p>
      </div>
      <footer>
        <p>© 2025 SpotR. All rights reserved.</p>
      </footer>
    </div>
  );
}
