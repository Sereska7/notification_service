import sys
import os

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

from app.pkg.connectors import PostgresSQL
from app.pkg.models.sqlalchemy_models import Base, Recipient, Message, EmailCorrespondent, TelegramCorrespondent, Delivery, TextTemplate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
print("Tables registered for Alembic:", target_metadata.tables.keys())

# Инициализируем контейнер
container = PostgresSQL()

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_sync_dsn() -> str:
    url = container.configuration.POSTGRES.DSN()
    url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    sync_dsn = get_sync_dsn()

    context.configure(
        url=sync_dsn,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    sync_dsn = get_sync_dsn()
    engine = create_engine(sync_dsn)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
