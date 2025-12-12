import React, { useEffect, useState } from "react";
import { logout,  getCurrentUser } from "../services/auth_api";

export default function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getCurrentUser()
      .then(res => {
        setUser(res.data); 
      })
      .catch(() => {
        window.location.href = "/"; 
      });
  }, []);

  const handleLogout = async () => {
    try {
      await logout();
      window.location.href = "/";
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  if (!user) return <p>Chargement...</p>;

  return (
    <div className="dashboard container">
      <h1>Welcome {user.display_name || "User"}</h1>
      <p>Here you can explore your musical mood and recent tracks.</p>
      <button className="logout" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

