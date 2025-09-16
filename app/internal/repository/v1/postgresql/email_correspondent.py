"""EmailCorrespondent repository implementation."""

from sqlalchemy import select, update, func

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models import v1 as models
from app.pkg.models.sqlalchemy_models import EmailCorrespondent

__all__ = ["EmailCorrespondentRepository"]


class EmailCorrespondentRepository(Repository):
    """EmailCorrespondent repository implementation."""

    @collect_response
    async def create(
            self,
            cmd: models.EmailCorrespondentCreateCommand
    ) -> models.EmailCorrespondentResponse:
        """Creates a new email correspondent in the database.

        Args:
            cmd (models.EmailCorrespondentCreateCommand): Command containing data for correspondent creation.

        Returns:
            models.EmailCorrespondentResponse: The created email correspondent details.
        """

        async with get_connection() as session:
            correspondent = EmailCorrespondent(**cmd.to_dict())
            session.add(correspondent)
            await session.commit()
            await session.refresh(correspondent)

            return models.EmailCorrespondentResponse.model_validate(correspondent)

    @collect_response
    async def read(
            self,
            query: models.EmailCorrespondentReadQuery
    ) -> list[models.EmailCorrespondentResponse]:
        """Retrieves email correspondents matching the given filters.

        Args:
            query (models.EmailCorrespondentReadQuery): Query containing filters for retrieving correspondents.

        Returns:
            list[models.EmailCorrespondentResponse]: The list of email correspondents matching the filters.
        """

        async with get_connection() as session:
            stmt = (
                select(EmailCorrespondent)
                .where(
                    *(
                        [EmailCorrespondent.email_correspondent_id == query.email_correspondent_id]
                        if query.email_correspondent_id else []
                    ),
                    *(
                        [EmailCorrespondent.email_correspondent_name.ilike(
                            f"%{query.email_correspondent_name.strip()}%")]
                        if query.email_correspondent_name else []
                    ),
                    *(
                        [EmailCorrespondent.email_correspondent_is_active == query.email_correspondent_is_active]
                        if query.email_correspondent_is_active is not None else []
                    ),
                )
                .order_by(EmailCorrespondent.email_correspondent_create_at.desc())
            )
            rows = (await session.execute(stmt)).scalars().all()
            return rows

    @collect_response
    async def update(
            self,
            cmd: models.EmailCorrespondentUpdateCommand,
    ) -> models.EmailCorrespondentResponse:
        """Updates an existing email correspondent in the database.

        Args:
            cmd (models.EmailCorrespondentUpdateCommand): Command containing updated data for the correspondent.

        Returns:
            models.EmailCorrespondentResponse: The updated email correspondent details.
        """

        async with get_connection() as session:
            patch = cmd.model_dump(exclude_unset=True, exclude_none=True)
            patch.pop("email_correspondent_id", None)

            stmt = (
                update(EmailCorrespondent)
                .where(EmailCorrespondent.email_correspondent_id == cmd.email_correspondent_id)
                .values(**patch)
                .returning(EmailCorrespondent)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj

    @collect_response
    async def delete(
            self,
            cmd: models.EmailCorrespondentDeleteCommand
    ) -> models.EmailCorrespondentResponse:
        """Performs a soft delete of an email correspondent by setting it inactive.

        Args:
            cmd (models.EmailCorrespondentDeleteCommand): Command containing identifier of the correspondent to delete.

        Returns:
            models.EmailCorrespondentResponse: The deleted email correspondent details.
        """

        async with get_connection() as session:
            stmt = (
                update(EmailCorrespondent)
                .where(EmailCorrespondent.email_correspondent_id == cmd.email_correspondent_id)
                .values(
                    email_correspondent_is_active=False,
                    email_correspondent_update_at=func.now(),
                )
                .returning(EmailCorrespondent)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj
