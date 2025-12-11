import requests

BASE_URL = "https://api.spotify.com/v1"

def headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }

def get_profile(token):
    return requests.get(f"{BASE_URL}/me", headers=headers(token)).json()

def get_top_tracks(token):
    return requests.get(f"{BASE_URL}/me/top/tracks", headers=headers(token)).json()

def get_playlists(token):
    return requests.get(f"{BASE_URL}/me/playlists", headers=headers(token)).json()

def get_recent_tracks(token):
    return requests.get(f"{BASE_URL}/me/player/recently-played?limit=30", headers=headers(token)).json()

def get_audio_features(token, ids):
    joined = ",".join(ids)
    return requests.get(f"{BASE_URL}/audio-features?ids={joined}", headers=headers(token)).json()