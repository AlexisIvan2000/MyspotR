import pytest
from unittest.mock import patch, MagicMock


class TestClientRoutes:
    """Tests for Spotify client API routes."""

    def test_profile_without_login(self, client):
        """Test that /api/profile requires login."""
        response = client.get("/api/profile")
        assert response.status_code == 401
        assert b"Not logged in" in response.data

    @patch("routes.client_route.get_profile")
    @patch("routes.client_route.ensure_valid_token")
    def test_profile_with_login(self, mock_token, mock_profile, auth_client):
        """Test /api/profile with authenticated user."""
        mock_token.return_value = "valid_token"
        mock_profile.return_value = {
            "id": "spotify_user_id",
            "display_name": "Test User",
            "email": "test@example.com",
            "country": "CA",
            "images": [{"url": "https://example.com/image.jpg"}]
        }

        response = auth_client.get("/api/profile")
        assert response.status_code == 200

        data = response.get_json()
        assert data["display_name"] == "Test User"
        assert data["email"] == "test@example.com"

    def test_top_tracks_without_login(self, client):
        """Test that /api/top-tracks requires login."""
        response = client.get("/api/top-tracks")
        assert response.status_code == 401

    @patch("routes.client_route.get_top_tracks")
    @patch("routes.client_route.ensure_valid_token")
    def test_top_tracks_with_login(self, mock_token, mock_tracks, auth_client):
        """Test /api/top-tracks with authenticated user."""
        mock_token.return_value = "valid_token"
        mock_tracks.return_value = {
            "items": [
                {"id": "track1", "name": "Song 1"},
                {"id": "track2", "name": "Song 2"}
            ]
        }

        response = auth_client.get("/api/top-tracks")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["items"]) == 2
        assert data["items"][0]["name"] == "Song 1"

    def test_recent_tracks_without_login(self, client):
        """Test that /api/recent-tracks requires login."""
        response = client.get("/api/recent-tracks")
        assert response.status_code == 401

    @patch("routes.client_route.get_recent_tracks")
    @patch("routes.client_route.ensure_valid_token")
    def test_recent_tracks_with_login(self, mock_token, mock_recent, auth_client):
        """Test /api/recent-tracks with authenticated user."""
        mock_token.return_value = "valid_token"
        mock_recent.return_value = {
            "items": [
                {"track": {"id": "track1", "name": "Recent Song"}, "played_at": "2024-01-15T14:00:00Z"}
            ]
        }

        response = auth_client.get("/api/recent-tracks")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["items"]) == 1

    def test_playlists_without_login(self, client):
        """Test that /api/playlists requires login."""
        response = client.get("/api/playlists")
        assert response.status_code == 401

    @patch("routes.client_route.get_playlists")
    @patch("routes.client_route.ensure_valid_token")
    def test_playlists_with_login(self, mock_token, mock_playlists, auth_client):
        """Test /api/playlists with authenticated user."""
        mock_token.return_value = "valid_token"
        mock_playlists.return_value = {
            "items": [
                {"id": "playlist1", "name": "My Playlist", "tracks": {"total": 50}}
            ]
        }

        response = auth_client.get("/api/playlists")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["items"]) == 1
        assert data["items"][0]["name"] == "My Playlist"

    def test_audio_features_without_login(self, client):
        """Test that /api/audio-features requires login."""
        response = client.get("/api/audio-features?ids=track1,track2")
        assert response.status_code == 401

    def test_audio_features_without_ids(self, auth_client):
        """Test /api/audio-features without track IDs returns 400."""
        response = auth_client.get("/api/audio-features")
        assert response.status_code == 400
        assert b"No track IDs provided" in response.data

    @patch("routes.client_route.get_audio_features")
    @patch("routes.client_route.ensure_valid_token")
    def test_audio_features_with_ids(self, mock_token, mock_features, auth_client):
        """Test /api/audio-features with valid track IDs."""
        mock_token.return_value = "valid_token"
        mock_features.return_value = {
            "audio_features": [
                {"id": "track1", "energy": 0.8, "valence": 0.6},
                {"id": "track2", "energy": 0.3, "valence": 0.4}
            ]
        }

        response = auth_client.get("/api/audio-features?ids=track1,track2")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["audio_features"]) == 2


class TestSpotifyClientFunctions:
    """Tests for Spotify client service functions."""

    @patch("services.spotify_client.requests.get")
    def test_get_profile(self, mock_get):
        """Test get_profile function."""
        from services.spotify_client import get_profile

        mock_get.return_value.json.return_value = {"id": "user123", "display_name": "Test"}
        result = get_profile("test_token")

        mock_get.assert_called_once()
        assert "Authorization" in mock_get.call_args[1]["headers"]
        assert result["id"] == "user123"

    @patch("services.spotify_client.requests.get")
    def test_get_top_tracks(self, mock_get):
        """Test get_top_tracks function."""
        from services.spotify_client import get_top_tracks

        mock_get.return_value.json.return_value = {"items": []}
        result = get_top_tracks("test_token")

        assert "me/top/tracks" in mock_get.call_args[0][0]

    @patch("services.spotify_client.requests.get")
    def test_get_playlists(self, mock_get):
        """Test get_playlists function."""
        from services.spotify_client import get_playlists

        mock_get.return_value.json.return_value = {"items": []}
        result = get_playlists("test_token")

        assert "me/playlists" in mock_get.call_args[0][0]

    @patch("services.spotify_client.requests.get")
    def test_get_recent_tracks(self, mock_get):
        """Test get_recent_tracks function."""
        from services.spotify_client import get_recent_tracks

        mock_get.return_value.json.return_value = {"items": []}
        result = get_recent_tracks("test_token")

        assert "recently-played" in mock_get.call_args[0][0]
        assert "limit=30" in mock_get.call_args[0][0]

    @patch("services.spotify_client.requests.get")
    def test_get_audio_features(self, mock_get):
        """Test get_audio_features function."""
        from services.spotify_client import get_audio_features

        mock_get.return_value.json.return_value = {"audio_features": []}
        result = get_audio_features("test_token", ["id1", "id2"])

        assert "audio-features" in mock_get.call_args[0][0]
        assert "id1,id2" in mock_get.call_args[0][0]


class TestSpotifyAuthFunctions:
    """Tests for Spotify auth service functions."""

    def test_get_auth_url_format(self):
        """Test that auth URL has correct format."""
        from services.spotify_auth import get_auth_url

        url = get_auth_url()

        assert "accounts.spotify.com/authorize" in url
        assert "client_id=" in url
        assert "response_type=code" in url
        assert "redirect_uri=" in url
        assert "scope=" in url

    @patch("services.spotify_auth.requests.post")
    def test_get_token(self, mock_post):
        """Test get_token function."""
        from services.spotify_auth import get_token

        mock_post.return_value.json.return_value = {
            "access_token": "new_token",
            "refresh_token": "refresh",
            "expires_in": 3600
        }

        result = get_token("auth_code")

        mock_post.assert_called_once()
        assert result["access_token"] == "new_token"

    @patch("services.spotify_auth.requests.post")
    def test_refresh_access_token(self, mock_post):
        """Test refresh_access_token function."""
        from services.spotify_auth import refresh_access_token

        mock_post.return_value.json.return_value = {
            "access_token": "refreshed_token",
            "expires_in": 3600
        }

        result = refresh_access_token("old_refresh_token")

        mock_post.assert_called_once()
        assert "grant_type" in str(mock_post.call_args)
        assert result["access_token"] == "refreshed_token"


class TestRequireLoginDecorator:
    """Tests for require_login utility function."""

    def test_require_login_no_session(self, app):
        """Test require_login returns error when no session."""
        from utils.auth import require_login

        with app.test_request_context():
            user, error, status = require_login()
            assert user is None
            assert status == 401

    def test_require_login_invalid_user(self, app, client):
        """Test require_login returns 404 for invalid user."""
        from utils.auth import require_login

        with client.session_transaction() as sess:
            sess["user_id"] = 99999

        with app.test_request_context():
            from flask import session
            session["user_id"] = 99999
            user, error, status = require_login()
            assert user is None
            assert status == 404
