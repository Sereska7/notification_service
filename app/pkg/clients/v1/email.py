"""Models for Mail object."""

import datetime
import email
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.policy import default
from logging import Logger
from smtplib import SMTP, SMTPException
from bs4 import BeautifulSoup
from pydantic import EmailStr
from email.utils import parseaddr, formataddr

from app.pkg.logger import get_logger
from app.pkg.models import v1 as models


__all__ = ["EmailClient"]


class EmailClient:
    """MailService service."""

    __logger: Logger = get_logger(__name__)

    async def message_send_email(self, cmd: models.MessageSendCommand) -> bool:
        """Sends an email via SMTP.

        Args:
            cmd (models.SendEmailCommand): Email parameters, including sender, recipient, subject, body, and server details.

        Returns:
            bool: True if the email is sent successfully, False if an error occurs.
        """
        try:
            with SMTP(cmd.email_host, cmd.email_port, timeout=10) as smtp:
                self.__logger.debug("SMTP connection is successful")
                smtp.starttls()
                smtp.login(cmd.email_sender, cmd.email_password)
                self.__logger.debug("SMTP login is successful")

                msg = MIMEMultipart()
                msg["From"] = cmd.email_sender
                msg["To"] = ", ".join(str(email_item ) for email_item in [cmd.message_receiver])
                msg["Subject"] = cmd.text_template_subject
                msg.attach(MIMEText(cmd.text_template_content, "plain"))

                smtp.sendmail(
                    cmd.email_sender,
                    [str(email_item ) for email_item in [cmd.message_receiver]],
                    msg.as_string(),
                )
                self.__logger.info(
                    "Email sent successfully from %s to %s",
                    cmd.email_sender,
                    cmd.message_receiver,
                )
            return True
        except Exception as exc:
            self.__logger.exception(
                "Failed to send email from %s to %s. Error: %s",
                exc,
            )
            raise exc
