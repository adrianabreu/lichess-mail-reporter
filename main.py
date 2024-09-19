from lichess_mail_reporter.lichess import (
    get_games,
    parse_games,
    get_user_statistics,
    calculate_statistics,
)
from lichess_mail_reporter.mail_report import send_mail
from lichess_mail_reporter.config import Settings
from datetime import datetime, timedelta
from berserk import Client, utils

client = Client()
now = datetime.now()
start = utils.to_millis(now + timedelta(days=-7))
end = utils.to_millis(now)
settings = Settings()
user = settings.username

games = get_games(client, start, end, user)
parsed_games = parse_games(games, user)
user_stats = get_user_statistics(client, start, user)
stats = calculate_statistics(parsed_games, user_stats)

send_mail(
    sender_mail=settings.sender_mail,
    sender_name=settings.sender_name,
    recipients=settings.recipients,
    template_uuid=settings.template_uid,
    mail_token=settings.mail_token,
    data=dict(stats, username=user),
)
