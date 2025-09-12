"""Delivery models."""

from datetime import datetime
from uuid import UUID
from pydantic.fields import Field

from app.pkg.models.base import BaseModel, BaseEnum
from app.pkg.models.base.optional_field import create_optional_fields_class

__all__ = [
    "DeliveryStatusEnum"
]


class BaseDelivery(BaseModel):
    """Base model for Delivery."""


class DeliveryFields:
    """Delivery fields."""

class DeliveryStatusEnum(BaseEnum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"