"""Module with correspondent exceptions for the application."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "CorrespondentReadError",
    "CorrespondentNotFound",
    "CorrespondentCreateError",
    "CorrespondentDeleteError",
    "CorrespondentUpdateError",
    "CorrespondentAlreadyExists"
]


class CorrespondentNotFound(BaseAPIException):
    message = "Correspondent not found."
    status_code = status.HTTP_404_NOT_FOUND


class CorrespondentCreateError(BaseAPIException):
    message = "Error creating correspondent."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CorrespondentReadError(BaseAPIException):
    message = "Error reading correspondent."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CorrespondentDeleteError(BaseAPIException):
    message = "Error deleting correspondent."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class CorrespondentAlreadyExists(BaseAPIException):
    message = "Correspondent already exists."
    status_code = status.HTTP_409_CONFLICT


class CorrespondentUpdateError(BaseAPIException):
    message = "Error updating correspondent."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
