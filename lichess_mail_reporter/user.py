from typing import Any, Dict, List
from .client import LichessClient
from berserk import utils


def get_user_statistics(
    client: LichessClient, start_date: int, user: str
) -> List[Dict[str, Any]]:
    activity_feed = client.get_user_activity(user)
    parsed_data = [
        {"ts": item["interval"]["end"], "elo": item["games"]["blitz"]["rp"]["after"]}
        for item in activity_feed
    ]
    return list(filter(lambda x: utils.to_millis(x["ts"]) >= start_date, parsed_data))
