from flask import Blueprint, jsonify, request
from utils.auth import require_login
from services.spotify_client import (
    get_profile,
    get_top_tracks,
    get_recent_tracks,
    get_playlists,
    get_audio_features,
    ensure_valid_token
)
client_bp = Blueprint("client", __name__, url_prefix="/api")

@client_bp.route("/profile")
def api_profile():
    user, error_res, status = require_login()
    if error_res: 
        return error_res, status

    token = ensure_valid_token(user)
    data = get_profile(token)

    return jsonify(data)


@client_bp.route("/top-tracks")
def api_top_tracks():
    user, error_res, status = require_login()
    if error_res:
        return error_res, status

    token = ensure_valid_token(user)
    data = get_top_tracks(token)

    return jsonify(data)


@client_bp.route("/recent-tracks")
def api_recent_tracks():
    user, error_res, status = require_login()
    if error_res:
        return error_res, status

    token = ensure_valid_token(user)
    data = get_recent_tracks(token)

    return jsonify(data)


@client_bp.route("/playlists")
def api_playlists():
    user, error_res, status = require_login()
    if error_res:
        return error_res, status

    token = ensure_valid_token(user)
    data = get_playlists(token)

    return jsonify(data)


@client_bp.route("/audio-features")
def api_audio_features():
    user, error_res, status = require_login()
    if error_res:
        return error_res, status
    
    ids = request.args.get("ids")
    if not ids:
        return jsonify({"error": "No track IDs provided"}), 400

    token = ensure_valid_token(user)
    data = get_audio_features(token, ids.split(","))

    return jsonify(data)
