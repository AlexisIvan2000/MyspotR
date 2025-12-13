from flask import session, jsonify
from models.user import User

def require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None, jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    if not user:
        return None, jsonify({"error": "User not found"}), 404

    return user, None, None