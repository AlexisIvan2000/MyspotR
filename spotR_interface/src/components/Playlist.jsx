import { useEffect, useState } from "react";
import { getUserPlaylists } from "../services/spotify_api";

export default function Playlist() {
  const [playlists, setPlaylists] = useState(null);
  const [error, setError] = useState(null);

useEffect(() => {
  async function fetchPlaylists() {
    try {
      const res = await getUserPlaylists();

      console.log("PLAYLIST RES:", res);

      setPlaylists(res.items);
    } catch (err) {
      console.error(err);
      setError("Failed to load playlists");
    }
  }

  fetchPlaylists();
}, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!playlists) return <p>Loading playlists...</p>;

  return (
    <div className="playlist-grid">
      <h2>Your Playlists</h2>
      {playlists.map(pl => (
        <div key={pl.id} className="playlist-card" onClick={()=> window.open(pl.external_urls.spotify, "_blank")} >
          <img
            src={pl.images?.[0]?.url}
            alt={pl.name}
            style={{ width: 140, borderRadius: 12 }}
          />
          <h4 style={{ color: "white" }}>{pl.name}</h4>
          <p style={{ color: "#aaa" }}>{pl.tracks.total} tracks</p>
        </div>
      ))}
    </div>
  );
}
