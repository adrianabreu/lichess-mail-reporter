from typing import Any, Dict
from .client import LichessClient


def get_games(
    client: LichessClient, start_date: int, end_date: int, user: str
) -> list[Dict[str, Any]]:
    return client.get_games(user, start_date, end_date)


def get_first_move(moves, player_color):
    moves_list = moves.split()
    if player_color == "white":
        return moves_list[0] if moves_list else None
    elif player_color == "black":
        return moves_list[1] if len(moves_list) > 1 else None
    else:
        raise ValueError("Invalid player color. Use 'white' or 'black'.")


def parse_games(games: list[Dict[str, Any]], user: str) -> list[Dict[str, Any]]:
    parsed_games = [
        {
            "result": 1 if game["winner"] == color else 0,
            "first_move": get_first_move(game["moves"], color),
            "color": color,
        }
        for game in games
        for color in ("white", "black")
        if game["players"][color]["user"]["name"] == user
    ]
    return parsed_games
