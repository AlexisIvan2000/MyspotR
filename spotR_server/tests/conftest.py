import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from extensions import db
from models.user import User
from models.tokens import Tokens


@pytest.fixture
def app():
    
    application = Flask(__name__)
    application.config["SECRET_KEY"] = "test-secret-key"
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    application.config["TESTING"] = True
    application.config["SESSION_COOKIE_DOMAIN"] = None

    db.init_app(application)

    with application.app_context():
        from routes.auth_route import auth_bp
        from routes.client_auth import me_bp
        from routes.client_route import client_bp
        from routes.analysis_route import analysis_bp

        application.register_blueprint(auth_bp)
        application.register_blueprint(me_bp)
        application.register_blueprint(client_bp)
        application.register_blueprint(analysis_bp)

        db.create_all()

    yield application

    with application.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
 
    return app.test_client()


@pytest.fixture
def auth_client(app):
   
    with app.app_context():
        user = User(
            spotify_id="test_spotify_id",
            display_name="Test User",
            email="test@example.com",
            country="CA",
            profile_image_url="https://example.com/image.jpg"
        )
        db.session.add(user)
        db.session.commit()

        tokens = Tokens(
            user_id=user.id,
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            expires_in=3600
        )
        db.session.add(tokens)
        db.session.commit()

        user_id = user.id

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = user_id

    return client


@pytest.fixture
def sample_user(app):
    
    with app.app_context():
        user = User(
            spotify_id="sample_spotify_id",
            display_name="Sample User",
            email="sample@example.com",
            country="US",
            profile_image_url="https://example.com/sample.jpg"
        )
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_recent_tracks():
   
    return [
        {
            "track": {
                "id": "track1",
                "name": "Energetic Song",
                "popularity": 85,
                "explicit": True
            },
            "played_at": "2024-01-15T14:30:00Z"
        },
        {
            "track": {
                "id": "track2",
                "name": "Chill Song",
                "popularity": 40,
                "explicit": False
            },
            "played_at": "2024-01-15T23:30:00Z"
        },
        {
            "track": {
                "id": "track3",
                "name": "Medium Song",
                "popularity": 60,
                "explicit": False
            },
            "played_at": "2024-01-15T12:00:00Z"
        }
    ]
