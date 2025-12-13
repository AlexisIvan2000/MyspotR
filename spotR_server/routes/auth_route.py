from flask import Blueprint, redirect, request, session, jsonify
from services.spotify_auth import get_auth_url, get_token
from services.spotify_client import get_profile
from models.user import User
from models.tokens import Tokens
from extensions import db


auth_bp = Blueprint("auth", __name__, url_prefix="/auth/spotify")

@auth_bp.route("/login")
def login():
    auth_url = get_auth_url()
    return redirect(auth_url)


@auth_bp.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Error during authentication: {error}", 400
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    tokens = get_token(code)

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    expires_in = tokens.get("expires_in")

    profile = get_profile(access_token)

    spotify_id = profile["id"]
    email = profile.get("email")
    display_name = profile.get("display_name")
    country = profile.get("country")
    profile_image = profile["images"][0]["url"] if profile.get("images") else None

    user = User.query.filter_by(spotify_id=spotify_id).first()

    if not user:
        user = User(
            spotify_id=spotify_id,
            email=email,
            display_name=display_name,
            country=country,
            profile_image_url=profile_image
        )
        db.session.add(user)
        db.session.commit()

    tokens = Tokens.query.filter_by(user_id=user.id).first()

    if not tokens:
        tokens = Tokens(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )
        db.session.add(tokens)
    else:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in

    db.session.commit()
    session["user_id"] = user.id
    return redirect("http://127.0.0.1:5173/dashboard")

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

