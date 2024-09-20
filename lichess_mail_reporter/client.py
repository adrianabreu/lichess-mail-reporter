from berserk import Client
from typing import Any, Dict, List


class LichessClient:
    def __init__(self):
        self._client = Client()

    def get_games(
        self, user: str, start_date: int, end_date: int, max_games: int = 300
    ) -> List[Dict[str, Any]]:
        games = self._client.games.export_by_player(
            user, since=start_date, until=end_date, max=max_games
        )
        return list(games)

    def get_user_activity(self, user: str) -> List[Dict[str, Any]]:
        return self._client.users.get_activity_feed(user)
