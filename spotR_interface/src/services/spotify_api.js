import api  from "./auth_api";

export async function getSpotifyProfile() {
    return api.get("/api/profile");
}

export async function getTopTracks() {
    return api.get("/api/top-tracks");
}

export async function getRecentTracks() {
    return api.get("/api/recent-tracks");
}

export async function getUserPlaylists() {
    return api.get("/api/playlists");
}

export async function getAudioFeatures(ids)  {
    const query = ids.join(",");
    return api.get(`/api/audio-features?ids=${query}`);
}

export default {
  getSpotifyProfile,
  getTopTracks,
  getRecentTracks,
  getUserPlaylists,
  getAudioFeatures,
};