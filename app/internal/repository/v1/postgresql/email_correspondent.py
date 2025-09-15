"""EmailCorrespondent repository implementation."""

from uuid import UUID

from sqlalchemy import select, update

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models
from app.pkg.models.sqlalchemy_models import EmailCorrespondent
from app.pkg.models.v1.exceptions.repository import EmptyResult

__all__ = ["EmailCorrespondentRepository"]


class EmailCorrespondentRepository(Repository):
    """EmailCorrespondent repository implementation."""

    @collect_response
    async def create(self, cmd: models.EmailCorrespondentCreateCommand) -> models.EmailCorrespondentResponse:
        """
        """

        async with get_connection() as session:
            correspondent = EmailCorrespondent(**cmd.to_dict())
            session.add(correspondent)
            await session.commit()
            await session.refresh(correspondent)

            return models.EmailCorrespondentResponse.model_validate(correspondent)