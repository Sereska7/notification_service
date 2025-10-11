"""Models for Delivery object."""

from logging import Logger

from app.internal.repository.v1.postgresql import DeliveryRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult

__all__ = ["DeliveryService"]


class DeliveryService:
    """Recipient service class."""

    delivery_repository: DeliveryRepository
    __logger: Logger = get_logger(__name__)