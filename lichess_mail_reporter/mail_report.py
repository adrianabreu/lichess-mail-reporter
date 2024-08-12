import mailtrap as mt
from typing import Dict
import json
import logging

def send_mail(sender_mail: str, sender_name: str, recipients: list[str], template_uuid: str, mail_token: str, data: Dict[str, str]) -> None:
    try:
        mail = mt.MailFromTemplate(
        sender=mt.Address(email=sender_mail, name=sender_name),
        to=[mt.Address(email=mail) for mail in recipients],
        template_uuid=template_uuid,
        template_variables=data
        )

        client = mt.MailtrapClient(token=mail_token)
        
        client.send(mail)
        logging.info("Email sent successfully.")
    except mt.MailtrapError as e:
        logging.error(f"Failed to send email: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
