"""All postgresql repositories are defined here."""

from dependency_injector import containers, providers

from app.internal.repository.v1.postgresql.email_correspondent import EmailCorrespondentRepository
from app.internal.repository.v1.postgresql.telegram_correspondent import TelegramCorrespondentRepository
from app.internal.repository.v1.postgresql.text_template import TextTemplateRepository


class Repositories(containers.DeclarativeContainer):
    """Container for postgresql repositories."""

    email_correspondent_repository = providers.Factory(EmailCorrespondentRepository)
    telegram_correspondent_repository = providers.Factory(TelegramCorrespondentRepository)
    text_template_repository = providers.Factory(TextTemplateRepository)
