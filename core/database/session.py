"""
Модуль для управления асинхронными сессиями базы данных.

Предоставляет движок SQLAlchemy, фабрику сессий и dependency для FastAPI.
"""

from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.base.config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
"""Асинхронный движок SQLAlchemy с проверкой соединений перед использованием."""

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
"""Фабрика асинхронных сессий с отключённым autocommit и autoflush."""


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency для получения асинхронной сессии базы данных.

    Используется как FastAPI dependency для внедрения сессии БД в обработчики.
    Автоматически закрывает сессию после завершения запроса.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.
    """
    async with async_session_maker() as session:
        yield session
