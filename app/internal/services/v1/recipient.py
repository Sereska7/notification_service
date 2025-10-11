"""Models for Recipient object."""

from logging import Logger

from app.internal.repository.v1.postgresql import RecipientRepository
from app.pkg.logger import get_logger
from app.pkg.models import v1 as models
from app.pkg.models.v1.exceptions.repository import DriverError, EmptyResult

__all__ = ["RecipientService"]


class RecipientService:
    """Recipient service class."""

    recipient_repository: RecipientRepository
    __logger: Logger = get_logger(__name__)