from flask import Blueprint,  jsonify
from models.user import User
from services.spotify_client import (
    get_recent_tracks,
    get_audio_features,
    ensure_valid_token
)
from services.mood_analysis import mood_from_features
from flask import session

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

def get_logged_user():
    user_id = session.get("user_id")
    if not user_id:
        return None, jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user:
        return None, jsonify({"error": "User not found"}), 404

    return user, None, None

@analysis_bp.route('/mood')
def mood():
    user, error, status = get_logged_user()
    if error:
        return error, status
    
    token = ensure_valid_token(user)
    recent = get_recent_tracks(token)
    items = recent.get('items', [])

    if not items:
        return jsonify({"error": "No recent tracks found"}), 404
    
    ids = [
        item['track']['id']
        for item in items
        if item.get('track') 
    ]
    features = get_audio_features(token, ids).get('audio_features', [])
    mood_data = mood_from_features(features)
    if not mood_data:
        return jsonify({"error": "Could not analyze mood"}), 400
    return jsonify(mood_data)
        