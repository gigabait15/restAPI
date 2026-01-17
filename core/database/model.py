from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""Базовый класс для декларативных моделей SQLAlchemy."""

__all__ = (
    "BaseIDModel",
    "Base",
)


class BaseIDModel:
    """
    Базовый миксин для моделей с ID и полями аудита.

    Предоставляет стандартные поля для всех моделей:
        - id: Первичный ключ с автоинкрементом.
        - created_at: Дата и время создания записи.
        - updated_at: Дата и время последнего обновления.
        - deleted_at: Дата и время мягкого удаления (soft delete).
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, index=True, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
