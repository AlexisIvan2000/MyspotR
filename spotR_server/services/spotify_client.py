import requests
from app import db
from services.spotify_auth import refresh_access_token

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

def ensure_valid_token(user):
    tokens = user.tokens

    if not tokens.access_token:
        refreshed = refresh_access_token(tokens.refresh_token)

        if "access_token" not in refreshed:
            raise Exception("Failed to refresh Spotify token")

        tokens.access_token = refreshed["access_token"]
        tokens.expires_in = refreshed.get("expires_in")
        db.session.commit()

    return tokens.access_token

