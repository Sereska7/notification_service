"""Message models."""

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr
from pydantic.fields import Field

from app.pkg.models.base import BaseModel, BaseEnum
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "MessageStatusEnum",
    "ChannelEnum",
    "MessageVerified",
    "MessageSendCommand"
]


class BaseMessage(BaseModel):
    """Base model for Message."""


class MessageFields:
    """Message fields."""

    event: str = Field(
        default="user.verification.requested",
        description="Type of the event. Always 'user.verification.requested'.",
        examples=["user.verification.requested"],
    )

    event_id: UUID = Field(
        description="Unique identifier of the event (UUID) used for idempotency.",
        examples=["a8d39bb4-0c52-4c56-a21b-34ed4b3f1570"],
    )

    occurred_at: datetime = Field(
        description="Timestamp (UTC) when the event was generated.",
        examples=["2025-09-09T14:10:11.532000+00:00"],
    )

    verification_id: UUID = Field(
        description="UUID of the verification record (key in Redis/DB).",
        examples=["4f7f6f6d-91e7-43aa-bb2f-3dcfb6a2edc4"],
    )
    verification_code: str = Field(
        description="Six-digit verification verification_code (or a magic link).",
        examples=["582341"],
        min_length=6,
        max_length=6,
    )
    user_id: UUID = Field(
        description="Unique identifier of the user.",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    user_email: EmailStr = Field(
        description="Email address of the user.",
        examples=["lolekeektop1@mail.ru", "user@example.com"],
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
    email_host: str = Field(
        description="SMTP-сервер для исходящей почты.",
        examples=["smtp.gmail.com", "smtp.yourapp.io"],
    )
    email_port: int = Field(
        description="Порт SMTP сервера.",
        ge=1, le=65535,
        examples=[465, 587],
    )
    email_sender: str = Field(
        description="Имя пользователя для авторизации на SMTP сервере.",
        examples=["support@yourapp.io"],
    )
    email_password: str = Field(
        description="Пароль или app password для SMTP.",
        examples=["••••••••"],
    )

class MessageStatusEnum(BaseEnum):
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    PARTIAL_FAILED = "partial_failed"
    FAILED = "failed"


class ChannelEnum(BaseEnum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


class MessageVerified(BaseMessage):
    """"""

    event: str = MessageFields.event
    event_id: UUID = MessageFields.event_id
    occurred_at: datetime = MessageFields.occurred_at
    verification_id: UUID = MessageFields.verification_id
    user_id: UUID = MessageFields.user_id
    email: EmailStr = MessageFields.user_email
    verification_code: str = MessageFields.verification_code


# Command.
class MessageSendCommand(BaseMessage):
    """"""

    email_host: str = MessageFields.email_host
    email_port: int = MessageFields.email_port
    email_sender: str = MessageFields.email_sender
    message_receiver: EmailStr = MessageFields.user_email
    email_password: str = MessageFields.email_password
    text_template_subject: str = MessageFields.text_template_subject
    text_template_content: str = MessageFields.text_template_content
