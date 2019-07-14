__author__ = 'Jakub Rachwalski'

from requests import post, Response
from typing import List
from models.user import error
import os
from dotenv import load_dotenv


class Mailgun:

    load_dotenv()
    MAILGUN_API = os.environ.get('MAILGUN_API', None)
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)
    FROM_NAME = "DoNotReply"
    FROM_EMAIL = f"<do-not-reply@{MAILGUN_DOMAIN}>"

    @classmethod
    def send_mail(cls, to: List[str], subject: str, text: str, html: str) -> Response:

        if cls.MAILGUN_API is None:
            raise error.MailgunException("Mailgun: API key does not exist")

        if cls.MAILGUN_DOMAIN is None:
            raise error.MailgunException("Mailgun: Domain does not exist")

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", f"{cls.MAILGUN_API}"),
            data={"from": f"{cls.FROM_NAME} {cls.FROM_EMAIL}",
                  "to": to,
                  "subject": subject,
                  "text": text,
                  "html": html
                  })

        if response.status_code != 200:
            print(response.json())
            raise error.MailgunException("Mailgun: Email could not be sent")

        return response
