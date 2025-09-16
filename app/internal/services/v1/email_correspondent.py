"""Models for EmailCorrespondent object."""

from logging import Logger
from passlib.handlers.bcrypt import bcrypt

from app.internal.repository.v1.postgresql import EmailCorrespondentRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.correspondent import CorrespondentCreateError, CorrespondentReadError, \
    CorrespondentUpdateError, CorrespondentNotFound, CorrespondentAlreadyExists, CorrespondentDeleteError
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult, UniqueViolation

__all__ = ["EmailCorrespondentService"]


class EmailCorrespondentService:
    """Email correspondent service class."""

    email_correspondent_repository: EmailCorrespondentRepository
    __logger: Logger = get_logger(__name__)

    async def create_correspondent(
        self,
        cmd: models.EmailCorrespondentCreateCommand
    ) -> models.EmailCorrespondentResponse:
        """Creates a new email correspondent.

        Args:
            cmd (models.EmailCorrespondentCreateCommand): Payload with correspondent details.

        Returns:
            models.EmailCorrespondentResponse: Created correspondent.
        """

        try:
            hashed_password = bcrypt.hash(cmd.email_password)
            cmd.email_password = hashed_password
            return await self.email_correspondent_repository.create(cmd)
        except UniqueViolation as exc:
            self.__logger.exception("Failed to create email correspondent")
            raise CorrespondentAlreadyExists from exc
        except DriverError as exc:
            self.__logger.exception("Failed to create email correspondent")
            raise CorrespondentCreateError from exc

    async def get_email_correspondent(
        self,
        query: models.EmailCorrespondentReadQuery
    ) -> list[models.EmailCorrespondentResponse]:
        """Retrieves email correspondents by optional filters.

        Args:
            query (models.EmailCorrespondentReadQuery): Filters such as id, name, and is_active.

        Returns:
            list[models.EmailCorrespondentResponse]: Matching correspondents.
        """

        try:
            return await self.email_correspondent_repository.read(query)
        except DriverError as exc:
            self.__logger.exception("Failed to read email correspondents")
            raise CorrespondentReadError from exc

    async def update_email_correspondent(
        self,
        cmd: models.EmailCorrespondentUpdateCommand,
    ) -> models.EmailCorrespondentResponse:
        """Updates an email correspondent by id (partial update).

        Args:
            cmd (models.EmailCorrespondentUpdateCommand): Fields to update for the given correspondent id.

        Returns:
            models.EmailCorrespondentResponse: Updated correspondent.
        """

        try:
            return await self.email_correspondent_repository.update(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to update email correspondent")
            raise CorrespondentNotFound from exc
        except UniqueViolation as exc:
            self.__logger.exception("Failed to update email correspondent")
            raise CorrespondentAlreadyExists from exc
        except DriverError as exc:
            self.__logger.exception("Failed to update email correspondent")
            raise CorrespondentUpdateError from exc

    async def delete_email_correspondent(
        self,
        cmd: models.EmailCorrespondentDeleteCommand,
    ) -> models.EmailCorrespondentResponse:
        """Soft-deletes (deactivates) an email correspondent.

        Args:
            cmd (models.EmailCorrespondentDeleteCommand): Target correspondent id.

        Returns:
            models.EmailCorrespondentResponse: Deactivated correspondent (is_active = False).
        """

        try:
            return await self.email_correspondent_repository.delete(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to delete email correspondent")
            raise CorrespondentNotFound from exc
        except DriverError as exc:
            self.__logger.exception("Failed to delete email correspondent")
            raise CorrespondentDeleteError from exc
