"""V1 service layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.repository.v1 import postgresql, rabbitmq, redis
from app.internal.services.v1.telegram_correspondent_service import TelegramCorrespondentService
from app.internal.services.v1.email_correspondent import EmailCorrespondentService
from app.pkg.clients import Clients
from app.pkg.settings import settings


class Services(containers.DeclarativeContainer):
    """Containers with services."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    rabbitmq_repositories: rabbitmq.Repositories = providers.Container(
        Repositories.v1.rabbitmq,
    )  # type: ignore
    redis_repositories: redis.RedisRepositories = providers.Container(
        Repositories.v1.redis,
    )  # type: ignore

    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    clients: Clients = providers.Container(Clients)

    email_correspondent_service = providers.Factory(EmailCorrespondentService)
    email_correspondent_service.add_attributes(
        correspondent_repository=postgres_repositories.email_correspondent_repository,
    )

    telegram_correspondent_service = providers.Factory(TelegramCorrespondentService)
    telegram_correspondent_service.add_attributes(
        telegram_correspondent_repository=postgres_repositories.telegram_correspondent_repository,
    )
