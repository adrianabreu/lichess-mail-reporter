import pytest
from lichess_mail_reporter.client import LichessClient
from lichess_mail_reporter.game import (
    get_first_move,
    parse_games,
)


@pytest.fixture
def mock_lichess_client(mocker):
    mock = mocker.Mock(spec=LichessClient)
    return mock


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
