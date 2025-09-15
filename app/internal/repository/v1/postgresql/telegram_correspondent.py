"""TelegramCorrespondentRepository repository implementation."""

from uuid import UUID

from sqlalchemy import select, update

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models
from app.pkg.models.sqlalchemy_models import EmailCorrespondent
from app.pkg.models.sqlalchemy_models.v1.telegram_correspondent import TelegramCorrespondent
from app.pkg.models.v1.exceptions.repository import EmptyResult

__all__ = ["TelegramCorrespondentRepository"]


class TelegramCorrespondentRepository(Repository):
    """TelegramCorrespondentRepository repository implementation."""

    @collect_response
    async def create(
        self,
        cmd: models.TelegramCorrespondentCreateCommand
    ) -> models.TelegramCorrespondentResponse:
        """
        """

        async with get_connection() as session:
            correspondent = TelegramCorrespondent(**cmd.to_dict())
            session.add(correspondent)
            await session.commit()
            await session.refresh(correspondent)

            return models.TelegramCorrespondentResponse.model_validate(correspondent)