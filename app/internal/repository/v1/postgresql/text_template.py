"""Text template repository implementation."""

from sqlalchemy import select, update, func

from app.internal.repository.repository import Repository
from app.internal.repository.v1.postgresql.connection import get_connection
from app.internal.repository.v1.postgresql.handlers.collect_response import (
    collect_response,
)
from app.pkg.models.sqlalchemy_models import TextTemplate
from app.pkg.models import v1 as models

__all__ = ["TextTemplateRepository"]


class TextTemplateRepository(Repository):
    """Text template repository implementation."""

    @collect_response
    async def create(
        self,
        cmd: models.TextTemplateCreateCommand,
    ) -> models.TextTemplate:
        """Creates a new text template in the database.

        Args:
            cmd (models.TextTemplateCreateCommand): Command containing the data for the new template.

        Returns:
            models.TextTemplate: The created text template.
        """
        async with get_connection() as session:
            text_template = TextTemplate(**cmd.to_dict())
            session.add(text_template)
            await session.commit()
            await session.refresh(text_template)

            return models.TextTemplate.model_validate(text_template)

    @collect_response
    async def read(
        self,
        query: models.TextTemplateReadQuery
    ) -> list[models.TextTemplate]:
        """Reads text templates from the database based on query filters.

        Args:
            query (models.TextTemplateReadQuery): Query with optional filters
                (id, code, subject, is_active, channel).

        Returns:
            list[models.TextTemplate]: A list of matching text templates.
        """
        async with get_connection() as session:
            stmt = (
                select(TextTemplate)
                .where(
                    *(
                        [TextTemplate.text_template_id == query.text_template_id]
                        if query.text_template_id else []
                    ),
                    *(
                        [TextTemplate.text_template_code.ilike(
                            f"%{query.text_template_code.strip()}%")]
                        if query.text_template_code else []
                    ),
                    *(
                        [TextTemplate.text_template_subject == query.text_template_subject]
                        if query.text_template_subject else []
                    ),
                    *(
                        [TextTemplate.text_template_is_active == query.text_template_is_active]
                        if query.text_template_is_active else []
                    ),
                    *(
                        [TextTemplate.text_template_channel == query.text_template_channel]
                        if query.text_template_channel is not None else []
                    ),
                )
                .order_by(TextTemplate.text_template_create_at.desc())
            )
            rows = (await session.execute(stmt)).scalars().all()
            return rows

    @collect_response
    async def read_by_code(
        self,
        query: models.TextTemplateReadByCodeQuery
    ) -> models.TextTemplate:
        """"""

        async with get_connection() as session:
            stmt = (
                select(TextTemplate)
                .where(TextTemplate.text_template_code == query.text_template_code)
            )
            res = await session.execute(stmt)
            row = res.scalar_one()
            return row

    @collect_response
    async def update(
        self,
        cmd: models.TextTemplateUpdateCommand,
    ) -> models.TextTemplate:
        """Updates an existing text template in the database.

        Args:
            cmd (models.TextTemplateUpdateCommand): Command with the template ID and
                fields to be updated.

        Returns:
            models.TextTemplate: The updated text template, or None if not found.
        """
        async with get_connection() as session:
            patch = cmd.model_dump(exclude_unset=True, exclude_none=True)
            patch.pop("email_correspondent_id", None)

            stmt = (
                update(TextTemplate)
                .where(TextTemplate.text_template_id == cmd.text_template_id)
                .values(**patch)
                .returning(TextTemplate)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj

    @collect_response
    async def delete(
        self,
        cmd: models.TextTemplateDeleteCommand,
    ) -> models.TextTemplate:
        """Soft deletes (deactivates) a text template by setting is_active to False.

        Args:
            cmd (models.TextTemplateDeleteCommand): Command with the template ID.

        Returns:
            models.TextTemplate: The deactivated text template, or None if not found.
        """
        async with get_connection() as session:
            stmt = (
                update(TextTemplate)
                .where(TextTemplate.text_template_id == cmd.text_template_id)
                .values(
                    text_template_is_active=False,
                    text_template_update_at=func.now(),
                )
                .returning(TextTemplate)
            )
            res = await session.execute(stmt)
            obj = res.scalar_one_or_none()

            await session.commit()
            return obj

