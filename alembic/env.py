import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool import NullPool
from alembic import context
from config import ASYNC_DB_URL
from database.entities import User, Frequency, Sub
from database.connect import Base


# Настройка логирования из Alembic ini-файла
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Подключаем метаданные моделей для автогенерации
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме."""
    context.configure(
        url=ASYNC_DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме (асинхронно)."""
    connectable: AsyncEngine = create_async_engine(ASYNC_DB_URL, poolclass=NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Запуск миграций в синхронном режиме внутри асинхронного контекста."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
