from lichess_mail_reporter.client import LichessClient
from lichess_mail_reporter.game import get_games, parse_games
from lichess_mail_reporter.user import get_user_statistics
from lichess_mail_reporter.lichess import calculate_statistics

from lichess_mail_reporter.mail_report import send_mail
from lichess_mail_reporter.config import Settings
from datetime import datetime, timedelta
from berserk import utils


def main():
    now = datetime.now()
    start = utils.to_millis(now + timedelta(days=-7))
    end = utils.to_millis(now)
    settings = Settings()
    client = LichessClient()

    games = get_games(client, start, end, settings.username)
    parsed_games = parse_games(games, settings.username)
    user_stats = get_user_statistics(client, start, settings.username)
    stats = calculate_statistics(parsed_games, user_stats)

    send_mail(
        sender_mail=settings.sender_mail,
        sender_name=settings.sender_name,
        recipients=settings.recipients,
        template_uuid=settings.template_uid,
        mail_token=settings.mail_token,
        data=dict(stats, username=settings.username),
    )


if __name__ == "__main__":
    main()
