"""Models for Text template object."""

from logging import Logger

from app.internal.repository.v1.postgresql.text_template import TextTemplateRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult

__all__ = ["TextTemplateService"]

from app.pkg.models.v1.exceptions.text_template import TextTemplateCreateError, TextTemplateReadError, \
    TextTemplateUpdateError, TextTemplateNotFound, TextTemplateDeleteError


class TextTemplateService:
    """Text template service class."""

    text_template_repository: TextTemplateRepository
    __logger: Logger = get_logger(__name__)

    async def create_text_template(
        self,
        cmd: models.TextTemplateCreateCommand
    ) -> models.TextTemplate:
        """Creates a new text template.

        Args:
            cmd (models.TextTemplateCreateCommand): Command containing the data for template creation.

        Returns:
            models.TextTemplate: The created text template object.
        """

        try:
            return await self.text_template_repository.create(cmd)
        except DriverError as exc:
            self.__logger.exception("Failed to create text template.")
            raise TextTemplateCreateError from exc

    async def get_text_template(
        self,
        query: models.TextTemplateReadQuery
    ) -> list[models.TextTemplate]:
        """Retrieves text templates based on provided filters.

        Args:
            query (models.TextTemplateReadQuery): Query with filters for searching templates.

        Returns:
            list[models.TextTemplate]: A list of matched text templates.
        """

        try:
            return await self.text_template_repository.read(query)
        except DriverError as exc:
            self.__logger.exception("Failed to read text template.")
            raise TextTemplateReadError from exc

    async def update_text_template(
        self,
        cmd: models.TextTemplateUpdateCommand
    ) -> models.TextTemplate:
        """Updates an existing text template.

        Args:
            cmd (models.TextTemplateUpdateCommand): Command containing updated template data.

        Returns:
            models.TextTemplate: The updated text template object.
        """

        try:
            return await self.text_template_repository.update(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to update text template.")
            raise TextTemplateNotFound from exc
        except DriverError as exc:
            self.__logger.exception("Failed to update text template.")
            raise TextTemplateUpdateError from exc

    async def delete_text_template(
        self,
        cmd: models.TextTemplateDeleteCommand
    ) -> models.TextTemplate:
        """Soft deletes (deactivates) a text template.

        Args:
            cmd (models.TextTemplateDeleteCommand): Command with the identifier of the template to delete.

        Returns:
            models.TextTemplate: The text template object after deletion.
        """

        try:
            return await self.text_template_repository.delete(cmd)
        except EmptyResult as exc:
            self.__logger.exception("Failed to delete text template.")
            raise TextTemplateNotFound from exc
        except DriverError as exc:
            self.__logger.exception("Failed to delete text template.")
            raise TextTemplateDeleteError from exc
