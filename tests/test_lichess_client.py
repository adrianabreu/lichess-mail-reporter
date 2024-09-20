import pytest
from unittest.mock import MagicMock, patch
from lichess_mail_reporter.client import LichessClient


@pytest.fixture
def mock_berserk_client():
    with patch("berserk.Client") as mock_client:
        # Create a MagicMock for the games attribute
        mock_client.return_value.games = MagicMock()
        # Create a MagicMock for the users attribute
        mock_client.return_value.users = MagicMock()
        yield mock_client.return_value


@pytest.fixture
def lichess_client(mock_berserk_client):
    with patch("lichess_mail_reporter.client.Client", return_value=mock_berserk_client):
        return LichessClient()


class TestLichessClient:
    @pytest.mark.parametrize(
        "user,start,end,max_games,expected_games",
        [
            ("user1", 1640995200000, 1643673600000, 300, [{"id": 1}, {"id": 2}]),
            ("user2", 1640995200000, 1643673600000, 100, [{"id": 3}]),
            ("user3", 1640995200000, 1643673600000, 500, []),
        ],
    )
    def test_get_games(
        self,
        lichess_client,
        mock_berserk_client,
        user,
        start,
        end,
        max_games,
        expected_games,
    ):
        mock_berserk_client.games.export_by_player.return_value = expected_games

        games = lichess_client.get_games(user, start, end, max_games)

        mock_berserk_client.games.export_by_player.assert_called_once_with(
            user, since=start, until=end, max=max_games
        )
        assert games == expected_games

    @pytest.mark.parametrize(
        "user,expected_activity",
        [
            ("user1", [{"type": "game", "id": 1}, {"type": "puzzle", "id": 2}]),
            ("user2", []),
            (
                "user3",
                [
                    {"type": "game", "id": 3},
                    {"type": "game", "id": 4},
                    {"type": "puzzle", "id": 5},
                ],
            ),
        ],
    )
    def test_get_user_activity(
        self, lichess_client, mock_berserk_client, user, expected_activity
    ):
        mock_berserk_client.users.get_activity_feed.return_value = expected_activity

        activity = lichess_client.get_user_activity(user)

        mock_berserk_client.users.get_activity_feed.assert_called_once_with(user)
        assert activity == expected_activity
