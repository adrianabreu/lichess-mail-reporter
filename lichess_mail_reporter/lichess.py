
from typing import Any, Dict, List
from berserk import Client, utils
from collections import Counter


def get_games(
    berserk: Client, start_date: int, end_date: int, user: str
) -> list[Dict[str, Any]]:
    games = berserk.games.export_by_player(
        user, since=start_date, until=end_date, max=300
    )
    return list(games)


def get_user_statistics(
    berserk: Client, start_date: int, user: str
) -> List[Dict[str, Any]]:
    activity_feed = berserk.users.get_activity_feed(user)
    parsed_data = [
        {"ts": item["interval"]["end"], "elo": item["games"]["blitz"]["rp"]["after"]}
        for item in activity_feed
    ]
    return list(filter(lambda x: utils.to_millis(x["ts"]) >= start_date, parsed_data))


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


def calculate_statistics(parsed_games, user_stats) -> Dict[str, Any]:
    total_games = len(parsed_games)

    def count_games(condition):
        return sum(condition(game) for game in parsed_games)

    total_wins = count_games(lambda game: game["result"])
    total_white_games = count_games(lambda game: game["color"] == "white")
    total_black_games = total_games - total_white_games
    total_white_wins = count_games(
        lambda game: game["result"] and game["color"] == "white"
    )
    total_black_wins = total_wins - total_white_wins

    def get_first_moves(color):
        return [game["first_move"] for game in parsed_games if game["color"] == color]

    def get_most_frequent_move(moves):
        return Counter(moves).most_common(1)[0] if moves else None

    white_first_moves = get_first_moves("white")
    black_first_moves = get_first_moves("black")

    def format_move(move):
        return f"{move[0]} ({move[1]} times)" if move else None

    def safe_ratio(numerator, denominator):
        return round(numerator / denominator, 2) if denominator > 0 else 0

    statistics = {
        "total_played_games": total_games,
        "winning_ratio": safe_ratio(total_wins, total_games),
        "winning_ratio_as_white": safe_ratio(total_white_wins, total_white_games),
        "winning_ratio_as_black": safe_ratio(total_black_wins, total_black_games),
        "most_frequent_first_move_as_white": format_move(
            get_most_frequent_move(white_first_moves)
        ),
        "most_frequent_first_move_as_black": format_move(
            get_most_frequent_move(black_first_moves)
        ),
        "wins": total_wins,
        "loses": total_games - total_wins,
        "days_played": "'"
        + "','".join(x["ts"].strftime("%Y-%m-%d") for x in user_stats)
        + "'",
        "elo": "'" + "','".join(str(x["elo"]) for x in user_stats) + "'",
    }

    return statistics
