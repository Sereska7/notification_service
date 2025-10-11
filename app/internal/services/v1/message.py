"""Models for Message object."""

from logging import Logger

from app.internal.repository.v1.postgresql.message import MessageRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult

__all__ = ["MessageService"]


class MessageService:
    """Recipient service class."""

    message_repository: MessageRepository
    __logger: Logger = get_logger(__name__)

