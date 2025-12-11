import base64
import requests
from config import Config

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

def get_auth_url():
    return(
        f"{AUTH_URL}?client_id={Config.CLIENT_ID}"
        f"&response_type=code&redirect_uri={Config.REDIRECT_URI}"
        f"&scope=user-read-private user-read-email playlist-read-private "
        f"user-top-read user-read-recently-played"
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