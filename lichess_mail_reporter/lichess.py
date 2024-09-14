from datetime import datetime
from typing import Any, Dict
from berserk import Client
from collections import Counter
import plotly.graph_objects as go
import base64


def get_games(
    berserk: Client, start_date: datetime, end_date: datetime, user: str
) -> list[Dict[str, Any]]:
    games = berserk.games.export_by_player(
        user, since=start_date, until=end_date, max=300
    )
    return list(games)


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


def calculate_statistics(parsed_games) -> Dict[str, Any]:
    total_games = len(parsed_games)
    total_wins = sum(game["result"] for game in parsed_games)
    total_white_games = sum(game["color"] == "white" for game in parsed_games)
    total_black_games = sum(game["color"] == "black" for game in parsed_games)
    total_white_wins = sum(
        game["result"] for game in parsed_games if game["color"] == "white"
    )
    total_black_wins = sum(
        game["result"] for game in parsed_games if game["color"] == "black"
    )

    white_first_moves = [
        game["first_move"] for game in parsed_games if game["color"] == "white"
    ]
    black_first_moves = [
        game["first_move"] for game in parsed_games if game["color"] == "black"
    ]

    most_frequent_white_move = (
        Counter(white_first_moves).most_common(1)[0] if white_first_moves else None
    )
    most_frequent_black_move = (
        Counter(black_first_moves).most_common(1)[0] if black_first_moves else None
    )

    statistics = {
        "total_played_games": total_games,
        "winning_ratio": round(total_wins / total_games, 2) if total_games > 0 else 0,
        "winning_ratio_as_white": round(total_white_wins / total_white_games, 2)
        if total_white_games > 0
        else 0,
        "winning_ratio_as_black": round(total_black_wins / total_black_games, 2)
        if total_black_games > 0
        else 0,
        "most_frequent_first_move_as_white": f"{most_frequent_white_move[0]} ({most_frequent_white_move[1]} times)"
        if most_frequent_white_move
        else None,
        "most_frequent_first_move_as_black": f"{most_frequent_black_move[0]} ({most_frequent_black_move[1]} times)"
        if most_frequent_black_move
        else None,
    }

    return statistics


def add_graphs(statistics: Dict[str, Any]) -> Dict[str, Any]:
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=["Wins", "Losses"],
            values=[
                statistics["total_played_games"],
                statistics["total_played_games"] - statistics["total_played_games"],
            ],
        )
    )
    png = fig.to_image(format="png", engine="kaleido")
    png_base64 = base64.b64encode(png).decode("ascii")
    statistics["graph_winning_ratio"] = png_base64
    return statistics
