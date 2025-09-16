"""Message models."""

from datetime import datetime
from uuid import UUID

from pydantic.fields import Field

from app.pkg.models.base import BaseModel, BaseEnum
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "MessageStatusEnum",
    "ChannelEnum"
]


class BaseMessage(BaseModel):
    """Base model for Message."""


class MessageFields:
    """Message fields."""

class MessageStatusEnum(BaseEnum):
    PENDING = "pending"
    SENDING = "sending"
    SENT = "sent"
    PARTIAL_FAILED = "partial_failed"
    FAILED = "failed"


class ChannelEnum(BaseEnum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"
