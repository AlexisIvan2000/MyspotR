import pytest
from unittest.mock import patch
from services.mood_analysis import analyze_mood_from_recent, aggregate_by_day


class TestMoodAnalysis:
    """Tests for mood analysis functions."""

    def test_analyze_empty_recent_returns_unknown(self):
        """Test that empty recent tracks returns Unknown mood."""
        result = analyze_mood_from_recent([])
        assert result["label"] == "Unknown"
        assert result["score"] == 0
        assert result["timeline"] == []

    def test_analyze_none_recent_returns_unknown(self):
        """Test that None recent tracks returns Unknown mood."""
        result = analyze_mood_from_recent(None)
        assert result["label"] == "Unknown"

    def test_analyze_energetic_track(self):
        """Test that high popularity + explicit + daytime = Energetic."""
        recent = [{
            "track": {
                "popularity": 85,
                "explicit": True
            },
            "played_at": "2024-01-15T14:00:00Z"  # 14h = daytime
        }]
        result = analyze_mood_from_recent(recent)
        assert result["timeline"][0]["label"] == "Energetic"
        assert result["energy"] == 1
        assert result["calm"] == 0

    def test_analyze_chill_track(self):
        """Test that low popularity + not explicit + nighttime = Chill."""
        recent = [{
            "track": {
                "popularity": 30,
                "explicit": False
            },
            "played_at": "2024-01-15T23:00:00Z"  # 23h = nighttime
        }]
        result = analyze_mood_from_recent(recent)
        assert result["timeline"][0]["label"] == "Chill"
        assert result["calm"] == 1
        assert result["energy"] == 0

    def test_analyze_popularity_scoring(self):
        """Test popularity scoring logic."""
        high_pop = [{
            "track": {"popularity": 75, "explicit": False},
            "played_at": "2024-01-15T12:00:00Z"
        }]
        result = analyze_mood_from_recent(high_pop)
        assert result["timeline"][0]["score"] >= 2  # +2 for pop>70, +1 for daytime

        medium_pop = [{
            "track": {"popularity": 55, "explicit": False},
            "played_at": "2024-01-15T20:00:00Z"  # neutral hour
        }]
        result = analyze_mood_from_recent(medium_pop)
        assert result["timeline"][0]["score"] == 1  # +1 for pop>50

        low_pop = [{
            "track": {"popularity": 30, "explicit": False},
            "played_at": "2024-01-15T20:00:00Z"
        }]
        result = analyze_mood_from_recent(low_pop)
        assert result["timeline"][0]["score"] == -1  # -1 for low pop

    def test_analyze_explicit_adds_score(self):
        """Test that explicit content adds to score."""
        explicit_track = [{
            "track": {"popularity": 50, "explicit": True},
            "played_at": "2024-01-15T20:00:00Z"
        }]
        non_explicit_track = [{
            "track": {"popularity": 50, "explicit": False},
            "played_at": "2024-01-15T20:00:00Z"
        }]

        explicit_result = analyze_mood_from_recent(explicit_track)
        non_explicit_result = analyze_mood_from_recent(non_explicit_track)

        assert explicit_result["timeline"][0]["score"] > non_explicit_result["timeline"][0]["score"]

    def test_analyze_nighttime_reduces_score(self):
        """Test that nighttime (22-6) reduces score."""
        night_track = [{
            "track": {"popularity": 60, "explicit": False},
            "played_at": "2024-01-15T23:00:00Z"  # 23h
        }]
        day_track = [{
            "track": {"popularity": 60, "explicit": False},
            "played_at": "2024-01-15T14:00:00Z"  # 14h
        }]

        night_result = analyze_mood_from_recent(night_track)
        day_result = analyze_mood_from_recent(day_track)

        assert night_result["timeline"][0]["score"] < day_result["timeline"][0]["score"]

    def test_analyze_final_label_based_on_majority(self):
        """Test that final label is based on majority of tracks."""
        mostly_energetic = [
            {"track": {"popularity": 80, "explicit": True}, "played_at": "2024-01-15T14:00:00Z"},
            {"track": {"popularity": 85, "explicit": True}, "played_at": "2024-01-15T15:00:00Z"},
            {"track": {"popularity": 30, "explicit": False}, "played_at": "2024-01-15T23:00:00Z"}
        ]
        result = analyze_mood_from_recent(mostly_energetic)
        assert result["label"] == "Energetic"
        assert result["energy"] > result["calm"]

    def test_analyze_timeline_limited_to_20(self):
        """Test that timeline is limited to last 20 tracks."""
        many_tracks = [
            {"track": {"popularity": 50}, "played_at": f"2024-01-{(i % 28) + 1:02d}T{i % 24:02d}:00:00Z"}
            for i in range(25)
        ]
        result = analyze_mood_from_recent(many_tracks)
        assert len(result["timeline"]) == 20

    def test_analyze_missing_played_at(self):
        """Test handling of missing played_at field."""
        track_no_time = [{
            "track": {"popularity": 60, "explicit": False},
            "played_at": None
        }]
        result = analyze_mood_from_recent(track_no_time)
        assert result["timeline"][0]["hour"] is None


class TestAggregateByDay:
    """Tests for aggregate_by_day function."""

    def test_aggregate_empty_timeline(self):
        """Test aggregation with empty timeline."""
        result = aggregate_by_day([])
        assert result == {}

    def test_aggregate_day_tracks(self):
        """Test aggregation of daytime tracks (8-20)."""
        timeline = [
            {"hour": 10, "label": "Energetic"},
            {"hour": 14, "label": "Energetic"},
            {"hour": 18, "label": "Chill"}
        ]
        result = aggregate_by_day(timeline)
        assert "day" in result
        assert result["day"] == "Energetic"

    def test_aggregate_night_tracks(self):
        """Test aggregation of nighttime tracks."""
        timeline = [
            {"hour": 22, "label": "Chill"},
            {"hour": 23, "label": "Chill"},
            {"hour": 2, "label": "Energetic"}
        ]
        result = aggregate_by_day(timeline)
        assert "night" in result
        assert result["night"] == "Chill"

    def test_aggregate_mixed_day_night(self):
        """Test aggregation with both day and night tracks."""
        timeline = [
            {"hour": 10, "label": "Energetic"},
            {"hour": 14, "label": "Energetic"},
            {"hour": 22, "label": "Chill"},
            {"hour": 23, "label": "Chill"}
        ]
        result = aggregate_by_day(timeline)
        assert result["day"] == "Energetic"
        assert result["night"] == "Chill"

    def test_aggregate_skips_none_hours(self):
        """Test that None hours are skipped."""
        timeline = [
            {"hour": None, "label": "Energetic"},
            {"hour": 14, "label": "Chill"}
        ]
        result = aggregate_by_day(timeline)
        assert "day" in result
        assert result["day"] == "Chill"


class TestMoodRouteIntegration:
    """Integration tests for /api/analysis/mood route."""

    def test_mood_route_without_login(self, client):
        """Test that mood route requires login."""
        response = client.get("/api/analysis/mood")
        assert response.status_code == 401

    @patch("routes.analysis_route.get_recent_tracks")
    @patch("routes.analysis_route.ensure_valid_token")
    def test_mood_route_with_login(self, mock_token, mock_recent, auth_client):
        """Test mood route with authenticated user."""
        mock_token.return_value = "valid_token"
        mock_recent.return_value = {
            "items": [
                {
                    "track": {"popularity": 80, "explicit": True},
                    "played_at": "2024-01-15T14:00:00Z"
                }
            ]
        }

        response = auth_client.get("/api/analysis/mood")
        assert response.status_code == 200

        data = response.get_json()
        assert "label" in data
        assert "timeline" in data
        assert "by_period" in data

    @patch("routes.analysis_route.get_recent_tracks")
    @patch("routes.analysis_route.ensure_valid_token")
    def test_mood_route_no_recent_tracks(self, mock_token, mock_recent, auth_client):
        """Test mood route when no recent tracks."""
        mock_token.return_value = "valid_token"
        mock_recent.return_value = {"items": []}

        response = auth_client.get("/api/analysis/mood")
        assert response.status_code == 400
        assert b"No recent tracks" in response.data
