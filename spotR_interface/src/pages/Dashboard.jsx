import React from "react";
import ProfileUser from "../components/ProfileUser.jsx";
import TopTracks from "../components/TopTracks.jsx";
import Playlists from "../components/Playlist.jsx";
import MoodGraph from "../components/MoodGraph.jsx";
import { logout } from "../services/auth_api.js";

export default function Dashboard() {
  
  const handleLogout = async () => {
    await logout();
    window.location.href = "/";
  };

  return (
    <div className="dashboard-page">
      <aside className="sidebar">
        <ProfileUser />
        <nav className="menu">
          <h3>Contact Me</h3>
          <a href="https://www.linkedin.com/in/alexis-moungang-396104371">Linkedln</a>
          <a href="https://www.snapchat.com/add/alexis_ivan00?share_id=bmC_7yVomHY&locale=en-CA">Snapchat</a>
          <a href="https://github.com/AlexisIvan2000">GitHub</a>
          
        </nav>

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </aside>
      <main className="dashboard-content">     
        <MoodGraph />
        <section className="grid-two">
          <TopTracks />
          <Playlists />
        </section>

      </main>

    </div>
  );
}

