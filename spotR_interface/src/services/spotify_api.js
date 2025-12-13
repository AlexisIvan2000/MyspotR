import api from "./auth_api.js";

export async function safeGet(url) {
    try {
        const res = await api.get(url);
        return res.data;
    } catch (err) {
        console.error(`Error fetching ${url}`, err);
        throw err;
    }
}

export function getSpotifyProfile() {
    return safeGet("/api/profile");
}

export function getTopTracks() {
    return safeGet("/api/top-tracks");
}

export function getRecentTracks() {
    return safeGet("/api/recent-tracks");
}

export function getUserPlaylists() {
    return safeGet("/api/playlists");
}

export function getAudioFeatures(ids) {
    const query = ids.join(",");
    return safeGet(`/api/audio-features?ids=${query}`);
}

export async function getMoodAnalysis() {
    return api.get("/api/analysis/mood")
}

export default {
    getSpotifyProfile,
    getTopTracks,
    getRecentTracks,
    getUserPlaylists,
    getAudioFeatures,
};
