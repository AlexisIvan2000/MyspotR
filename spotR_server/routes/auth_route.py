from flask import Blueprint, redirect, request, session
from services.spotify_auth import get_auth_url, get_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth/spotify")

@auth_bp.route("/login")
def login():
    auth_url = get_auth_url()
    return redirect(auth_url)

@auth_bp.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Spotify error: {error}", 400

    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    tokens = get_token(code)
    session["access_token"] = tokens.get("access_token")
    session["refresh_token"] = tokens.get("refresh_token")
    session["expires_in"] = tokens.get("expires_in")
    return redirect("http://localhost:3000/dashboard")
