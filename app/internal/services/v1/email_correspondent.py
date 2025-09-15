"""Models for EmailCorrespondent object."""

from logging import Logger
from uuid import UUID
from passlib.handlers.bcrypt import bcrypt

from fastapi import Response

from app.internal.repository.v1.postgresql import EmailCorrespondentRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult
from app.pkg.settings import settings

__all__ = ["EmailCorrespondentService"]


class EmailCorrespondentService:
    """Auth service class."""

    email_correspondent_repository: EmailCorrespondentRepository
    __logger: Logger = get_logger(__name__)

    async def create_correspondent(
        self,
        cmd: models.EmailCorrespondentCreateCommand
    ) -> models.EmailCorrespondentResponse:
        """Create a new correspondent."""

        try:
            hashed_password = bcrypt.hash(cmd.email_password)
            cmd.email_password = hashed_password
            return await self.email_correspondent_repository.create(cmd)
        except Exception as exc:
            self.__logger.error(exc)
            raise exc
        except DriverError as exc:
            self.__logger.error(exc)
            raise exc