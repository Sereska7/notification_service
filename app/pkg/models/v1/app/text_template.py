"""Text templite models."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "TextTemplate",
    "TextTemplateCreateCommand",
    "TextTemplateUpdateCommand",
    "TextTemplateDeleteCommand",
    "TextTemplateReadQuery"
]

from app.pkg.models.v1 import ChannelEnum


class BaseTextTemplate(BaseModel):
    """Base model for text template."""


class TextTemplateFields:
    """TextTemplate fields."""

    text_template_id: UUID = Field(
        description="Уникальный идентификатор текстового шаблона.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )

    text_template_code: str = Field(
        description="Код (уникальный ключ) шаблона для поиска и идентификации.",
        min_length=1,
        max_length=200,
        examples=["welcome_email", "reset_password_sms"],
    )

    text_template_is_active: bool = Field(
        description="Флаг активности. Если False — шаблон не используется.",
        examples=[True, False],
    )

    text_template_subject: str = Field(
        description="Тема сообщения (используется для email-шаблонов).",
        examples=["Подтверждение регистрации", "Восстановление пароля"],
    )

    text_template_content: str = Field(
        description="Основной текст шаблона. Может содержать переменные в виде {{var}}.",
        examples=[
            "Здравствуйте, {{username}}! Подтвердите почту: {{code}}",
            "Ваш код подтверждения: {{code}}",
        ],
    )

    text_template_variables: dict[str, Any] = Field(
        description="JSON-словарь с перечнем переменных и их описанием.",
        examples=[{"username": "string",
                   "confirm_link": "url"}]
    )

    text_template_channel: ChannelEnum = Field(
        description="Канал, для которого предназначен шаблон.",
        examples=["email", "telegram", "sms"],
    )

    text_template_create_at: datetime = Field(
        description="Дата и время создания шаблона.",
        examples=["2024-09-12T10:15:30Z"],
    )

    text_template_update_at: datetime = Field(
        description="Дата и время последнего обновления шаблона.",
        examples=["2024-09-15T18:45:00Z"],
    )


OptionalTextTemplateFields = create_optional_fields_class(TextTemplateFields)


class TextTemplate(BaseTextTemplate):
    """Text template model."""

    text_template_id: UUID = TextTemplateFields.text_template_id
    text_template_code: str = TextTemplateFields.text_template_code
    text_template_is_active: bool = TextTemplateFields.text_template_is_active
    text_template_subject: str | None = OptionalTextTemplateFields.text_template_subject
    text_template_content: str = TextTemplateFields.text_template_content
    text_template_variables: dict[str, Any] | None = OptionalTextTemplateFields
    text_template_channel: ChannelEnum = TextTemplateFields.text_template_channel
    text_template_create_at: datetime = TextTemplateFields.text_template_update_at
    text_template_update_at: datetime | None = OptionalTextTemplateFields.text_template_update_at


# Command.
class TextTemplateCreateCommand(BaseTextTemplate):
    """Text template create command."""

    text_template_code: str = TextTemplateFields.text_template_code
    text_template_subject: str | None = OptionalTextTemplateFields.text_template_subject
    text_template_content: str = TextTemplateFields.text_template_content
    text_template_variables: dict[str, Any] | None = OptionalTextTemplateFields
    text_template_channel: ChannelEnum = TextTemplateFields.text_template_channel


class TextTemplateUpdateCommand(BaseTextTemplate):
    """Text template update command."""

    text_template_id: UUID = TextTemplateFields.text_template_id
    text_template_code: str | None = OptionalTextTemplateFields.text_template_code
    text_template_subject: str | None = OptionalTextTemplateFields.text_template_subject
    text_template_content: str | None = OptionalTextTemplateFields.text_template_content
    text_template_variables: dict[str, Any] | None = OptionalTextTemplateFields
    text_template_channel: ChannelEnum | None = OptionalTextTemplateFields.text_template_channel


class TextTemplateDeleteCommand(BaseTextTemplate):
    """Text template delete command."""

    text_template_id: UUID = TextTemplateFields.text_template_id


# Query.
class TextTemplateReadQuery(BaseTextTemplate):
    """Text template read query."""

    text_template_id: UUID | None = OptionalTextTemplateFields.text_template_id
    text_template_is_active: bool | None = OptionalTextTemplateFields.text_template_is_active
    text_template_code: str | None = OptionalTextTemplateFields.text_template_code
    text_template_subject: str | None = OptionalTextTemplateFields.text_template_subject
    text_template_channel: ChannelEnum | None = OptionalTextTemplateFields.text_template_channel
