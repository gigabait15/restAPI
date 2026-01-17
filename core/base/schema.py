from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

__all__ = (
    "BaseSchema",
    "BaseCreateSchema",
    "BaseUpdateSchema",
    "BaseReadSchema",
    "ResponseSchema",
    "ResponseListSchema",
)

T = TypeVar("T")


class BaseSchema(BaseModel):
    """
    Базовая схема Pydantic для всех схем приложения.

    Настройки:
        - from_attributes: Позволяет создавать схемы из ORM объектов.
        - str_strip_whitespace: Автоматически обрезает пробелы в строках.
        - strict: Строгая проверка типов.
    """

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        strict=True,
    )


class BaseCreateSchema(BaseSchema):
    """Базовая схема для создания объектов."""

    pass


class BaseUpdateSchema(BaseSchema):
    """
    Базовая схема для обновления объектов.

    Запрещает передачу дополнительных полей (extra="forbid").
    """

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        strict=True,
        extra="forbid",
    )

    def get_update_dict(self) -> dict:
        """
        Получить словарь только с установленными полями.

        Исключает поля, которые не были явно переданы при создании схемы.

        Returns:
            dict: Словарь с установленными полями для обновления.
        """
        return self.model_dump(exclude_unset=True)


class BaseReadSchema(BaseSchema):
    """
    Базовая схема для чтения объектов.

    Содержит стандартные поля аудита: id, created_at, updated_at, deleted_at.
    """

    id: int
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class ResponseSchema(BaseModel, Generic[T]):
    """
    Обёртка для единичного ответа API.

    Attributes:
        data: Данные ответа произвольного типа T.
    """

    data: T


class ResponseListSchema(BaseModel, Generic[T]):
    """
    Обёртка для списочного ответа API.

    Attributes:
        data: Список данных произвольного типа T.
    """

    data: list[T]
