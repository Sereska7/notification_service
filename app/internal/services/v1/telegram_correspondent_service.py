"""Models for TelegramCorrespondent object."""

from logging import Logger

from app.internal.repository.v1.postgresql import TelegramCorrespondentRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.correspondent import CorrespondentCreateError, CorrespondentReadError, \
    CorrespondentUpdateError, CorrespondentNotFound, CorrespondentAlreadyExists, CorrespondentDeleteError
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult, UniqueViolation

__all__ = ["TelegramCorrespondentService"]


class TelegramCorrespondentService:
    """Auth service class."""

    telegram_correspondent_repository: TelegramCorrespondentRepository
    __logger: Logger = get_logger(__name__)

    async def create_telegram_correspondent(
            self,
            cmd: models.TelegramCorrespondentCreateCommand
    ) -> models.TelegramCorrespondentResponse:
        """Creates a new telegram correspondent.

        Args:
            cmd (models.TelegramCorrespondentCreateCommand): Command containing data for correspondent creation.

        Returns:
            models.TelegramCorrespondentResponse: The created telegram correspondent details.
        """

        try:
            return await self.telegram_correspondent_repository.create(cmd)
        except UniqueViolation as exc:
            self.__logger.exception("Failed to create telegram correspondent.")
            raise CorrespondentAlreadyExists from exc
        except DriverError as exc:
            self.__logger.exception("Failed to create telegram correspondent.")
            raise CorrespondentCreateError from exc

    async def get_telegram_correspondent(
            self,
            query: models.TelegramCorrespondentReadQuery
    ) -> list[models.TelegramCorrespondentResponse]:
        """Retrieves telegram correspondents matching the given filters.

        Args:
            query (models.TelegramCorrespondentReadQuery): Query containing filters for retrieving correspondents.

        Returns:
            list[models.TelegramCorrespondentResponse]: The list of telegram correspondents matching the filters.
        """

        try:
            return await self.telegram_correspondent_repository.read(query)
        except DriverError as exc:
            self.__logger.exception("Failed to read telegram correspondent.")
            raise CorrespondentReadError from exc

    async def update_telegram_correspondent(
            self,
            cmd: models.TelegramCorrespondentUpdateCommand
    ) -> models.TelegramCorrespondentResponse:
        """Updates an existing telegram correspondent.

        Args:
            cmd (models.TelegramCorrespondentUpdateCommand): Command containing updated data for the correspondent.

        Returns:
            models.TelegramCorrespondentResponse: The updated telegram correspondent details.
        """

        try:
            return await self.telegram_correspondent_repository.update(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to update telegram correspondent.")
            raise CorrespondentNotFound from exc
        except UniqueViolation as exc:
            self.__logger.exception("Failed to update telegram correspondent.")
            raise CorrespondentUpdateError from exc
        except DriverError as exc:
            self.__logger.exception("Failed to update telegram correspondent.")
            raise CorrespondentUpdateError from exc

    async def delete_telegram_correspondent(
            self,
            cmd: models.TelegramCorrespondentDeleteCommand
    ) -> models.TelegramCorrespondentResponse:
        """Deletes a telegram correspondent.

        Args:
            cmd (models.TelegramCorrespondentDeleteCommand): Command containing identifier of the correspondent to delete.

        Returns:
            models.TelegramCorrespondentResponse: The deleted telegram correspondent details.
        """

        try:
            return await self.telegram_correspondent_repository.delete(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to delete telegram correspondent.")
            raise CorrespondentDeleteError from exc
        except DriverError as exc:
            self.__logger.exception("Failed to delete telegram correspondent.")
            raise CorrespondentDeleteError from exc
