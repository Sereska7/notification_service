"""Models for TelegramCorrespondent object."""

from logging import Logger
from uuid import UUID
from passlib.handlers.bcrypt import bcrypt

from fastapi import Response

from app.internal.repository.v1.postgresql import TelegramCorrespondentRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult
from app.pkg.settings import settings

__all__ = ["TelegramCorrespondentService"]


class TelegramCorrespondentService:
    """Auth service class."""

    telegram_correspondent_repository: TelegramCorrespondentRepository
    __logger: Logger = get_logger(__name__)

    async def create_telegram_correspondent(
        self,
        cmd: models.TelegramCorrespondentCreateCommand
    ) -> models.TelegramCorrespondentResponse:
        """Create TelegramCorrespondent object."""

        try:
            return await self.telegram_correspondent_repository.create(cmd)
        except Exception as exc:
            raise exc
        except DriverError as exc:
            self.__logger.exception("Failed to create telegram_correspondent")
            raise exc