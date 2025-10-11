"""Worker layer."""

from dependency_injector import containers, providers

from app.internal.repository import Repositories
from app.internal.repository.v1 import postgresql, rabbitmq, redis
from app.internal.services import Services
from app.internal.workers.email_sender import EmailSenderWorker
from app.pkg.clients import Clients
from app.pkg.settings import settings

__all__ = ["Workers"]


class Workers(containers.DeclarativeContainer):
    """Consumers container."""

    configuration = providers.Configuration(name="settings")
    configuration.from_dict(settings.model_dump())

    services: Services = providers.Container(Services)
    clients: Clients = providers.Container(Clients)
    rabbitmq_repositories: rabbitmq.Repositories = providers.Container(
        Repositories.v1.rabbitmq,
    )  # type: ignore

    redis_repositories: redis.RedisRepositories = providers.Container(
        Repositories.v1.redis,
    )  # type: ignore

    postgres_repositories: postgresql.Repositories = providers.Container(
        Repositories.v1.postgres,
    )  # type: ignore

    mail_sender_worker = providers.Singleton(EmailSenderWorker)
    mail_sender_worker.add_attributes(
        redis_repository=redis_repositories.base_redis_repository,
        rabbitmq_repository=rabbitmq_repositories.base_repository,
        email_correspondent_repository=postgres_repositories.email_correspondent_repository,
        text_template_repository=postgres_repositories.text_template_repository,
        message_repository=postgres_repositories.message_repository,
        text_template_service=services.v1.text_template_service,
        mail_client=clients.v1.email_client,
    )
