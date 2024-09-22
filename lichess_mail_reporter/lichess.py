from typing import Any, Dict
from collections import Counter


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
        "days_played": ",".join(f"'{stat['ts'].strftime('%Y-%m-%d')}'" for stat in user_stats),
        "elo": ",".join(f"'{stat['elo']}'" for stat in user_stats),
    }

    return statistics
