import { useEffect, useState } from "react";
import { getSpotifyProfile } from "../services/spotify_api";

export default function ProfileUser() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await getSpotifyProfile();
        setProfile(data);
      } catch (err) {
        console.error("Failed to load profile", err);
      }
    }

    fetchProfile();
  }, []);

  if (!profile) return <p>Loading profile...</p>;

  return (
    <section className="card">
      <img src={profile.images?.[0]?.url} className="avatar" />
      <h3 className="profile-name">{profile.display_name}</h3>
      <p className="profile-email">{profile.email}</p>
      <p className="profile-country">{profile.country}</p>

      <a href={profile.external_urls.spotify} target="_blank" rel="noreferrer">
        See your Spotify Profile
      </a>
    </section>
  );
}
