"""TelegramCorrespondentRepository repository implementation."""

from sqlalchemy import select, update, func

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models
from app.pkg.models.sqlalchemy_models.v1.telegram_correspondent import TelegramCorrespondent

__all__ = ["TelegramCorrespondentRepository"]


class TelegramCorrespondentRepository(Repository):
    """TelegramCorrespondentRepository repository implementation."""

    @collect_response
    async def create(
        self,
        cmd: models.TelegramCorrespondentCreateCommand
    ) -> models.TelegramCorrespondentResponse:
        """Creates a new telegram correspondent in the database.

        Args:
            cmd (models.TelegramCorrespondentCreateCommand): Command containing data for correspondent creation.

        Returns:
            models.TelegramCorrespondentResponse: The created telegram correspondent details.
        """

        async with get_connection() as session:
            correspondent = TelegramCorrespondent(**cmd.to_dict())
            session.add(correspondent)
            await session.commit()
            await session.refresh(correspondent)

            return models.TelegramCorrespondentResponse.model_validate(correspondent)

    @collect_response
    async def read(
        self,
        query: models.TelegramCorrespondentReadQuery
    ) -> list[models.TelegramCorrespondentResponse]:
        """Retrieves telegram correspondents matching the given filters.

        Args:
            query (models.TelegramCorrespondentReadQuery): Query containing filters for retrieving correspondents.

        Returns:
            list[models.TelegramCorrespondentResponse]: The list of telegram correspondents matching the filters.
        """

        async with get_connection() as session:
            stmt = (
                select(TelegramCorrespondent)
                .where(
                    *(
                        [TelegramCorrespondent.telegram_correspondent_id == query.telegram_correspondent_id]
                        if query.telegram_correspondent_id else []
                    ),
                    *(
                        [TelegramCorrespondent.telegram_correspondent_name.ilike(
                            f"%{query.telegram_correspondent_name.strip()}%")]
                        if query.telegram_correspondent_name else []
                    ),
                    *(
                        [TelegramCorrespondent.telegram_correspondent_is_active == query.telegram_correspondent_is_active]
                        if query.telegram_correspondent_is_active is not None else []
                    ),
                )
                .order_by(TelegramCorrespondent.telegram_correspondent_create_at.desc())
            )
            rows = (await session.execute(stmt)).scalars().all()
            return rows

    @collect_response
    async def update(
        self,
        cmd: models.TelegramCorrespondentUpdateCommand
    ) -> models.TelegramCorrespondentResponse:
        """Updates an existing telegram correspondent in the database.

        Args:
            cmd (models.TelegramCorrespondentUpdateCommand): Command containing updated data for the correspondent.

        Returns:
            models.TelegramCorrespondentResponse: The updated telegram correspondent details.
        """

        async with get_connection() as session:
            patch = cmd.model_dump(exclude_unset=True, exclude_none=True)
            patch.pop("telegram_correspondent_id", None)

            stmt = (
                update(TelegramCorrespondent)
                .where(TelegramCorrespondent.telegram_correspondent_id == cmd.telegram_correspondent_id)
                .values(**patch)
                .returning(TelegramCorrespondent)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj

    @collect_response
    async def delete(
        self,
        cmd: models.TelegramCorrespondentDeleteCommand
    ) -> models.TelegramCorrespondentResponse:
        """Performs a soft delete of a telegram correspondent by setting it inactive.

        Args:
            cmd (models.TelegramCorrespondentDeleteCommand): Command containing identifier of the correspondent to delete.

        Returns:
            models.TelegramCorrespondentResponse: The deleted telegram correspondent details.
        """

        async with get_connection() as session:
            stmt = (
                update(TelegramCorrespondent)
                .where(TelegramCorrespondent.telegram_correspondent_id == cmd.telegram_correspondent_id)
                .values(
                    telegram_correspondent_is_active=False,
                    telegram_correspondent_update_at=func.now(),
                )
                .returning(TelegramCorrespondent)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj
