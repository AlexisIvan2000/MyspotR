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

      <ul className="track-list">
        {tracks.map((track) => (
          <li key={track.id}>
            <img src={track.album.images[2]?.url} />
            <span>{track.artists.map((artist) => artist.name).join(", ")}</span>
            <span>{track.name}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
