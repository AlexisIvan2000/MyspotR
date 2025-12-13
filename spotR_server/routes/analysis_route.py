from flask import Blueprint, jsonify
from utils.auth import require_login
from services.spotify_client import get_recent_tracks, ensure_valid_token
from services.mood_analysis import analyze_mood_from_recent, aggregate_by_day

analysis_bp = Blueprint("analysis", __name__, url_prefix="/api/analysis")

@analysis_bp.route("/mood")
def mood():
    user, error, status = require_login()
    if error:
        return error, status

    token = ensure_valid_token(user)
    recent_raw = get_recent_tracks(token)
    recent = recent_raw.get("items", [])

    if not recent:
        return jsonify({"error": "No recent tracks"}), 400

    result = analyze_mood_from_recent(recent)
    result["by_period"] = aggregate_by_day(result["timeline"])
    return jsonify(result)

