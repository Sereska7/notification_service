"""TelegramCorrespondent models."""

from datetime import datetime
from uuid import UUID
from pydantic.fields import Field

from app.pkg.models.base import BaseModel
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "TelegramCorrespondent",
    "TelegramCorrespondentResponse",
    "TelegramCorrespondentCreateCommand"
]


class BaseTelegramCorrespondent(BaseModel):
    """Base model for TelegramCorrespondent."""


class TelegramCorrespondentFields:
    """TelegramCorrespondent fields."""

    telegram_correspondent_id: UUID = Field(
        description="Уникальный идентификатор отправителя.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    telegram_correspondent_name: str = Field(
        description="Отображаемое имя отправителя.",
        min_length=1,
        max_length=200,
        examples=["Support Team"],
    )
    telegram_correspondent_is_active: bool = Field(
        default=True,
        description="Признак активности отправителя.",
        examples=[True],
    )
    telegram_bot_token: str = Field(
        description="Секретный токен бота, выданный @BotFather.",
        examples=["123456789:AAH7f5Lr2q8xYv9zQpZQ0w1e2r3t4y5u6v7w"],
    )
    telegram_correspondent_create_at: datetime = Field(
        description="Момент создания записи (UTC).",
        examples=["2025-09-13T12:34:56Z"],
    )
    telegram_correspondent_update_at: datetime | None = Field(
        default=None,
        description="Момент последнего обновления записи (UTC).",
        examples=[None, "2025-09-13T12:45:01Z"],
    )


OptionalTelegramCorrespondentFields = create_optional_fields_class(TelegramCorrespondentFields)


class TelegramCorrespondent(BaseTelegramCorrespondent):
    """TelegramCorrespondent model."""

    telegram_correspondent_id: UUID = TelegramCorrespondentFields.telegram_correspondent_id
    telegram_correspondent_name: str = TelegramCorrespondentFields.telegram_correspondent_name
    telegram_correspondent_is_active: bool = TelegramCorrespondentFields.telegram_correspondent_is_active
    telegram_bot_token: str = TelegramCorrespondentFields.telegram_bot_token
    telegram_correspondent_create_at: datetime = TelegramCorrespondentFields.telegram_correspondent_create_at
    telegram_correspondent_update_at: datetime | None = OptionalTelegramCorrespondentFields.telegram_correspondent_update_at


class TelegramCorrespondentResponse(BaseTelegramCorrespondent):
    """TelegramCorrespondentResponse model."""

    telegram_correspondent_id: UUID = TelegramCorrespondentFields.telegram_correspondent_id
    telegram_correspondent_name: str = TelegramCorrespondentFields.telegram_correspondent_name
    telegram_correspondent_is_active: bool = TelegramCorrespondentFields.telegram_correspondent_is_active
    telegram_correspondent_create_at: datetime = TelegramCorrespondentFields.telegram_correspondent_create_at
    telegram_correspondent_update_at: datetime | None = OptionalTelegramCorrespondentFields.telegram_correspondent_update_at


class TelegramCorrespondentCreateCommand(BaseTelegramCorrespondent):
    """TelegramCorrespondentCreateCommand model."""

    telegram_correspondent_name: str = TelegramCorrespondentFields.telegram_correspondent_name
    telegram_bot_token: str = TelegramCorrespondentFields.telegram_bot_token
