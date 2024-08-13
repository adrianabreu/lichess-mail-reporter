import pytest
from datetime import datetime
from berserk import Client
from lichess_mail_reporter.lichess import (
    get_games,
    get_first_move,
    parse_games,
    calculate_statistics,
)


@pytest.fixture
def mock_berserk(mocker):
    mock = mocker.Mock(spec=Client)
    mock.games = mocker.Mock()
    return mock


def test_get_games(mock_berserk):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    user = "test_user"

    mock_games = [{"id": 1}, {"id": 2}]
    mock_berserk.games.export_by_player.return_value = mock_games

    games = get_games(mock_berserk, start_date, end_date, user)

    mock_berserk.games.export_by_player.assert_called_once_with(
        user, since=start_date, until=end_date, max=300
    )
    assert games == mock_games


def test_get_first_move():
    moves = "e4 e5 kc3 kf6"
    assert get_first_move(moves, "white") == "e4"
    assert get_first_move(moves, "black") == "e5"
    assert get_first_move("", "white") is None
    assert get_first_move("e4", "black") is None


def test_parse_games():
    games = [
        {
            "winner": "white",
            "moves": "e4 e5",
            "players": {
                "white": {"user": {"name": "test_user"}},
                "black": {"user": {"name": "other_user"}},
            },
        },
        {
            "winner": "black",
            "moves": "d4 d5",
            "players": {
                "white": {"user": {"name": "other_user"}},
                "black": {"user": {"name": "test_user"}},
            },
        },
    ]
    user = "test_user"

    parsed_games = parse_games(games, user)

    expected = [
        {"result": 1, "first_move": "e4", "color": "white"},
        {"result": 1, "first_move": "d5", "color": "black"},
    ]
    assert parsed_games == expected


def test_calculate_statistics():
    parsed_games = [
        {"result": 1, "first_move": "e4", "color": "white"},
        {"result": 0, "first_move": "d4", "color": "white"},
        {"result": 1, "first_move": "d5", "color": "black"},
        {"result": 0, "first_move": "e5", "color": "black"},
    ]

    statistics = calculate_statistics(parsed_games)

    expected = {
        "total_played_games": 4,
        "winning_ratio": 0.5,
        "winning_ratio_as_white": 0.5,
        "winning_ratio_as_black": 0.5,
        "most_frequent_first_move_as_white": "e4 (1 times)",
        "most_frequent_first_move_as_black": "d5 (1 times)",
    }
    assert statistics == expected
