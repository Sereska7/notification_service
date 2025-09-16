"""EmailCorrespondent models."""

from datetime import datetime
from uuid import UUID
from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "EmailCorrespondent",
    "EmailCorrespondentResponse",
    "EmailCorrespondentCreateCommand",
    "EmailCorrespondentUpdateCommand",
    "EmailCorrespondentDeleteCommand",
    "EmailCorrespondentReadQuery",
]


class BaseEmailCorrespondent(BaseModel):
    """Base model for EmailCorrespondent."""


class EmailCorrespondentFields:
    """EmailCorrespondent fields."""

    email_correspondent_id: UUID = Field(
        description="Уникальный идентификатор отправителя.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    email_correspondent_name: str = Field(
        description="Отображаемое имя отправителя.",
        min_length=1,
        max_length=200,
        examples=["Support Team"],
    )
    email_correspondent_is_active: bool = Field(
        default=True,
        description="Признак активности отправителя.",
        examples=[True],
    )
    email_host: str = Field(
        description="SMTP-сервер для исходящей почты.",
        examples=["smtp.gmail.com", "smtp.yourapp.io"],
    )
    email_port: int = Field(
        description="Порт SMTP сервера.",
        ge=1, le=65535,
        examples=[465, 587],
    )
    email_username: str = Field(
        description="Имя пользователя для авторизации на SMTP сервере.",
        examples=["support@yourapp.io"],
    )
    email_password: str = Field(
        description="Пароль или app password для SMTP.",
        examples=["••••••••"],
    )
    email_correspondent_create_at: datetime = Field(
        description="Момент создания записи (UTC).",
        examples=["2025-09-13T12:34:56Z"],
    )
    email_correspondent_update_at: datetime | None = Field(
        default=None,
        description="Момент последнего обновления записи (UTC).",
        examples=[None, "2025-09-13T12:45:01Z"],
    )


OptionalEmailCorrespondentFields = create_optional_fields_class(EmailCorrespondentFields)


class EmailCorrespondent(BaseEmailCorrespondent):
    """EmailCorrespondent model."""

    email_correspondent_id: UUID = EmailCorrespondentFields.email_correspondent_id
    email_correspondent_name: str = EmailCorrespondentFields.email_correspondent_name
    email_host: str = EmailCorrespondentFields.email_host
    email_port: int = EmailCorrespondentFields.email_port
    email_username: str = EmailCorrespondentFields.email_username
    email_password: str = EmailCorrespondentFields.email_password
    email_correspondent_is_active: bool = EmailCorrespondentFields.email_correspondent_is_active
    email_correspondent_create_at: datetime = EmailCorrespondentFields.email_correspondent_create_at
    email_correspondent_update_at: datetime | None = EmailCorrespondentFields.email_correspondent_update_at


class EmailCorrespondentResponse(BaseEmailCorrespondent):
    """EmailCorrespondent response model."""

    email_correspondent_id: UUID = EmailCorrespondentFields.email_correspondent_id
    email_correspondent_name: str = EmailCorrespondentFields.email_correspondent_name
    email_host: str = EmailCorrespondentFields.email_host
    email_port: int = EmailCorrespondentFields.email_port
    email_username: str = EmailCorrespondentFields.email_username
    email_correspondent_is_active: bool = EmailCorrespondentFields.email_correspondent_is_active
    email_correspondent_create_at: datetime = EmailCorrespondentFields.email_correspondent_create_at
    email_correspondent_update_at: datetime | None = OptionalEmailCorrespondentFields.email_correspondent_update_at


# Command.
class EmailCorrespondentCreateCommand(BaseEmailCorrespondent):
    """EmailCorrespondent create command."""

    email_correspondent_name: str = EmailCorrespondentFields.email_correspondent_name
    email_host: str = EmailCorrespondentFields.email_host
    email_port: int = EmailCorrespondentFields.email_port
    email_username: str = EmailCorrespondentFields.email_username
    email_password: str = EmailCorrespondentFields.email_password


class EmailCorrespondentUpdateCommand(BaseEmailCorrespondent):
    """EmailCorrespondent update command."""

    email_correspondent_id: UUID = EmailCorrespondentFields.email_correspondent_id
    email_correspondent_name: str | None = OptionalEmailCorrespondentFields.email_correspondent_name
    email_host: str | None = OptionalEmailCorrespondentFields.email_host
    email_port: int | None = OptionalEmailCorrespondentFields.email_port
    email_username: str | None = OptionalEmailCorrespondentFields.email_username
    email_password: str | None = OptionalEmailCorrespondentFields.email_password


class EmailCorrespondentDeleteCommand(BaseEmailCorrespondent):
    """EmailCorrespondent delete command."""

    email_correspondent_id: UUID = EmailCorrespondentFields.email_correspondent_id


# Query.
class EmailCorrespondentReadQuery(BaseEmailCorrespondent):
    """EmailCorrespondent read query model."""

    email_correspondent_id: UUID | None = OptionalEmailCorrespondentFields.email_correspondent_id
    email_correspondent_name: str | None = OptionalEmailCorrespondentFields.email_correspondent_name
    email_correspondent_is_active: bool | None = OptionalEmailCorrespondentFields.email_correspondent_is_active
