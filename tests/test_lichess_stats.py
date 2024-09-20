from datetime import datetime
from lichess_mail_reporter.lichess import calculate_statistics


def test_calculate_statistics():
    parsed_games = [
        {"result": 1, "first_move": "e4", "color": "white"},
        {"result": 0, "first_move": "d4", "color": "white"},
        {"result": 1, "first_move": "d5", "color": "black"},
        {"result": 0, "first_move": "e5", "color": "black"},
        {"result": 0, "first_move": "e5", "color": "black"},
        {"result": 0, "first_move": "d4", "color": "white"},
    ]

    user_stats = [
        {"ts": datetime(2024, 9, 7), "elo": 1500},
        {"ts": datetime(2024, 9, 6), "elo": 1505},
    ]

    statistics = calculate_statistics(parsed_games, user_stats)

    expected = {
        "total_played_games": 6,
        "winning_ratio": 0.33,
        "winning_ratio_as_white": 0.33,
        "winning_ratio_as_black": 0.33,
        "most_frequent_first_move_as_white": "d4 (2 times)",
        "most_frequent_first_move_as_black": "e5 (2 times)",
        "wins": 2,
        "loses": 4,
        "days_played": "'2024-09-07','2024-09-06'",
        "elo": "'1500','1505'",
    }
    assert statistics == expected
