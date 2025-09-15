"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.v1.postgresql.email_correspondent import EmailCorrespondentRepository
from app.internal.repository.v1.postgresql.telegram_correspondent import TelegramCorrespondentRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    email_correspondent_repository = providers.Factory(EmailCorrespondentRepository)
    telegram_correspondent_repository = providers.Factory(TelegramCorrespondentRepository)
