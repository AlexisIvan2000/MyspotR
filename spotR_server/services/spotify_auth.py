import base64
import requests
from config import Config
import urllib.parse

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_auth_url():
    redirect = urllib.parse.quote(Config.REDIRECT_URI, safe="")
    scope = urllib.parse.quote(
        "user-read-private user-read-email playlist-read-private user-top-read user-read-recently-played user-read-playback-state user-read-currently-playing",
        safe=""
    )

    return (
        f"{AUTH_URL}?client_id={Config.CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect}"
        f"&scope={scope}"
    )

def get_token(code):
    auth_header = base64.b64encode(
        f"{Config.CLIENT_ID}:{Config.CLIENT_SECRET}".encode() 
    ).decode()

    response = requests.post(
        TOKEN_URL,
        data= {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Config.REDIRECT_URI
        },
        headers={
            "Authorization": f"Basic {auth_header}",
        }
    )
    return response.json()

def refresh_access_token(refresh_token):
    auth_header = base64.b64encode(
        f"{Config.CLIENT_ID}:{Config.CLIENT_SECRET}".encode()
    ).decode()

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        },
        headers={
            "Authorization": f"Basic {auth_header}"
        }
    )
    return response.json()
