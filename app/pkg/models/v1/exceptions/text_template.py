"""Module with text template exceptions for the application."""

from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = [
    "TextTemplateNotFound",
    "TextTemplateCreateError",
    "TextTemplateReadError",
    "TextTemplateUpdateError",
    "TextTemplateDeleteError"
]


class TextTemplateNotFound(BaseAPIException):
    message = "Text template not found."
    status_code = status.HTTP_404_NOT_FOUND


class TextTemplateCreateError(BaseAPIException):
    message = "Text template creating error."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class TextTemplateReadError(BaseAPIException):
    message = "Text template reading error."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class TextTemplateUpdateError(BaseAPIException):
    message = "Text template updating error."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class TextTemplateDeleteError(BaseAPIException):
    message = "Text template deleting error."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


