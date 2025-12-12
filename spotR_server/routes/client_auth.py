from flask import Blueprint, jsonify, session
from models.user import User
from models.tokens import Tokens

me_bp = Blueprint("me", __name__, url_prefix="/api")

@me_bp.route("/me")
def me():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "spotify_id": user.spotify_id,
        "display_name": user.display_name,
        "email": user.email,
        "country": user.country,
        "profile_image": user.profile_image_url
    })

