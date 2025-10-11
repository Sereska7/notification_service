"""Module for Mail sender worker."""

import json
from logging import Logger

from redis import RedisError

from app.internal.repository.v1 import redis
from app.internal.repository.v1.postgresql import EmailCorrespondentRepository, TextTemplateRepository, \
    MessageRepository
from app.internal.repository.v1.rabbitmq import BaseRepository
from app.internal.services.v1 import TextTemplateService
from app.pkg.clients.v1.email import EmailClient
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.base.exception import BaseClientException
from app.pkg.models.v1 import MessageStatusEnum
from app.pkg.models.v1.exceptions.correspondent import CorrespondentNotFound, CorrespondentReadError
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult
from app.pkg.models.v1.exceptions.text_template import TextTemplateNotFound, TextTemplateReadError
from app.pkg.settings import settings

__all__ = ["EmailSenderWorker"]


class EmailSenderWorker:
    """Mail sender worker.

    Manages email sending, message updates, and related processing.
    """

    redis_repository: redis.BaseRedisRepository
    rabbitmq_repository: BaseRepository
    email_correspondent_repository: EmailCorrespondentRepository
    text_template_repository: TextTemplateRepository
    message_repository: MessageRepository
    text_template_service: TextTemplateService
    mail_client: EmailClient
    __logger: Logger = get_logger(__name__)

    async def listen_sending_message(self):
        """Listen to the 'sending_message' queue and process incoming
        messages."""

        self.__logger.info("Start listen sending message")
        try:
            async for message in self.rabbitmq_repository.listen_queue(
                    routing_key=settings.RABBITMQ.NOTIFICATION_KEY,
            ):
                sending_message = models.MessageVerified(**message)
                await self.process_sending_message(sending_message)
        except Exception:
            self.__logger.exception("Error listen queue from RebbitMQ.")

    async def process_sending_message(
        self,
        sending_message: models.MessageVerified
    ):
        """Process sending message."""

        self.__logger.debug("Start process sending message")

        try:
            sender_message = await self.email_correspondent_repository.read_by_name(
                query=models.EmailCorrespondentReadByNameQuery(
                    email_correspondent_name=sending_message.event
                )
            )
        except EmptyResult:
            self.__logger.exception("Empty sender message.")
            raise CorrespondentNotFound
        except DriverError as exc:
            self.__logger.exception("Failed to read correspondent.")
            raise CorrespondentReadError from exc
        try:
            text_template = await self.text_template_repository.read_by_code(
                query=models.TextTemplateReadByCodeQuery(
                    text_template_code=sending_message.event,
                    text_template_channel=models.ChannelEnum.EMAIL
                )
            )
        except EmptyResult:
            self.__logger.exception("Empty text template message.")
            raise TextTemplateNotFound
        except DriverError as exc:
            self.__logger.exception("Failed to read text template.")
            raise TextTemplateReadError from exc

        try:
            context = {
                "username": sending_message.email,
                "verification_code": sending_message.verification_code,
            }
            render_template_content = await self.text_template_service.render_template_content(
                template=text_template,
                context=context,
            )
        except Exception as exc:
            self.__logger.exception("Error rendering template.")
            raise exc

        try:
            cmd = models.MessageSendCommand(
                email_host=sender_message.email_host,
                email_port=sender_message.email_port,
                email_sender=sender_message.email_username,
                message_receiver=sending_message.email,
                email_password=sender_message.email_password,
                text_template_subject=text_template.text_template_subject,
                text_template_content=render_template_content,
            )
            await self.mail_client.message_send_email(cmd)
        except Exception as exc:
            self.__logger.exception("Error send message message.")
            try:
                self.message_repository.message_update_status()
            raise exc
