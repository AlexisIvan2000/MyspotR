import pytest
from unittest.mock import patch, MagicMock
from models.user import User
from models.tokens import Tokens
from extensions import db


class TestAuthRoutes:
    """Tests for authentication routes."""

    def test_login_redirects_to_spotify(self, client):
        """Test that /auth/spotify/login redirects to Spotify."""
        response = client.get("/auth/spotify/login")
        assert response.status_code == 302
        assert "accounts.spotify.com/authorize" in response.location

    def test_login_url_contains_required_params(self, client):
        """Test that login URL contains required OAuth parameters."""
        response = client.get("/auth/spotify/login")
        location = response.location
        assert "client_id=" in location
        assert "response_type=code" in location
        assert "redirect_uri=" in location
        assert "scope=" in location

    def test_callback_without_code_returns_error(self, client):
        """Test that callback without code returns 400."""
        response = client.get("/auth/spotify/callback")
        assert response.status_code == 400
        assert b"No code provided" in response.data

    def test_callback_with_error_returns_error(self, client):
        """Test that callback with error parameter returns 400."""
        response = client.get("/auth/spotify/callback?error=access_denied")
        assert response.status_code == 400
        assert b"Error during authentication" in response.data

    @patch("routes.auth_route.get_token")
    @patch("routes.auth_route.get_profile")
    def test_callback_creates_new_user(self, mock_profile, mock_token, app, client):
        """Test that callback creates a new user when not exists."""
        mock_token.return_value = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600
        }
        mock_profile.return_value = {
            "id": "new_spotify_id",
            "email": "new@example.com",
            "display_name": "New User",
            "country": "FR",
            "images": [{"url": "https://example.com/new.jpg"}]
        }

        response = client.get("/auth/spotify/callback?code=test_code")

        assert response.status_code == 302
        assert "/dashboard" in response.location

        with app.app_context():
            user = User.query.filter_by(spotify_id="new_spotify_id").first()
            assert user is not None
            assert user.email == "new@example.com"
            assert user.display_name == "New User"

    @patch("routes.auth_route.get_token")
    @patch("routes.auth_route.get_profile")
    def test_callback_updates_existing_user_tokens(self, mock_profile, mock_token, app, client):
        """Test that callback updates tokens for existing user."""
        with app.app_context():
            user = User(
                spotify_id="existing_id",
                email="existing@example.com",
                display_name="Existing User",
                country="CA"
            )
            db.session.add(user)
            db.session.commit()

            tokens = Tokens(
                user_id=user.id,
                access_token="old_token",
                refresh_token="old_refresh",
                expires_in=3600
            )
            db.session.add(tokens)
            db.session.commit()

        mock_token.return_value = {
            "access_token": "updated_access_token",
            "refresh_token": "updated_refresh_token",
            "expires_in": 7200
        }
        mock_profile.return_value = {
            "id": "existing_id",
            "email": "existing@example.com",
            "display_name": "Existing User",
            "country": "CA",
            "images": []
        }

        response = client.get("/auth/spotify/callback?code=test_code")

        assert response.status_code == 302

        with app.app_context():
            user = User.query.filter_by(spotify_id="existing_id").first()
            assert user.tokens.access_token == "updated_access_token"

    def test_logout_clears_session(self, auth_client):
        """Test that logout clears the session."""
        response = auth_client.post("/auth/spotify/logout")
        assert response.status_code == 200
        assert b"Logged out successfully" in response.data

    def test_logout_without_session(self, client):
        """Test that logout works even without session."""
        response = client.post("/auth/spotify/logout")
        assert response.status_code == 200


class TestMeRoute:
    """Tests for /api/me route."""

    def test_me_without_login_returns_401(self, client):
        """Test that /api/me returns 401 when not logged in."""
        response = client.get("/api/me")
        assert response.status_code == 401
        assert b"Not logged in" in response.data

    def test_me_with_login_returns_user_data(self, app, auth_client):
        """Test that /api/me returns user data when logged in."""
        response = auth_client.get("/api/me")
        assert response.status_code == 200

        data = response.get_json()
        assert data["spotify_id"] == "test_spotify_id"
        assert data["display_name"] == "Test User"
        assert data["email"] == "test@example.com"

    def test_me_with_invalid_user_id_returns_404(self, app, client):
        """Test that /api/me returns 404 for invalid user_id in session."""
        with client.session_transaction() as sess:
            sess["user_id"] = 99999

        response = client.get("/api/me")
        assert response.status_code == 404
        assert b"User not found" in response.data
