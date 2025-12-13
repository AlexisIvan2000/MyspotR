import { useEffect, useState } from "react";
import api from "../services/auth_api";

export default function Recommendations({ mood }) {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!mood) return;

    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        setError(null);

        const res = await api.get(
          `/api/analysis/recommendations?mood=${mood}`
        );

        setTracks(res.data.tracks || []);
      } catch (err) {
        console.error(err);
        setError("Failed to load recommendations");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [mood]);

  if (loading) return <p>Loading recommendations...</p>;
  if (error) return <p>{error}</p>;
  if (!tracks.length) return <p>No recommendations found.</p>;

  return (
    <div className="card">
      <h2>🎧 Recommended for your mood</h2>

      <div className="tracks-grid">
        {tracks.map(track => (
          <a
            key={track.id}
            href={track.external_urls.spotify}
            target="_blank"
            rel="noreferrer"
            className="track-card"
          >
            <img
              src={track.album.images[0]?.url}
              alt={track.name}
            />
            <div className="track-info">
              <strong>{track.name}</strong>
              <span>
                {track.artists.map(a => a.name).join(", ")}
              </span>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
