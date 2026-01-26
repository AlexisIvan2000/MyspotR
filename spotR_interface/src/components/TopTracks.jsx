import { useEffect, useState } from "react";
import { getTopTracks } from "../services/spotify_api";

export default function TopTracks() {
  const [tracks, setTracks] = useState([]);

  useEffect(() => {
    getTopTracks().then((res) => {
      setTracks(res.items || []);
    });
  }, []);

  return (
    <section className="card">
      <h2>Top Tracks</h2>

      <div className="tracks-grid">
        {tracks.map((track) => (
          <div className="track-card" key={track.id}>
            <img src={track.album.images[1]?.url} alt={track.name} />
            <div className="track-info">
              <span className="track-artist">{track.artists.map((artist) => artist.name).join(", ")}</span>
              <span className="track-title">{track.name}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
