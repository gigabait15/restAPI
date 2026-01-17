from pydantic import BaseModel, Field

from core.base.schema import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema


class ActivityCreate(BaseCreateSchema):
    """Схема для создания деятельности."""

    name: str
    parent_id: int | None = None


class ActivityRead(BaseReadSchema):
    """Схема для чтения данных деятельности."""

    name: str
    parent_id: int | None = None
    level: int


class ActivityUpdate(BaseUpdateSchema):
    """Схема для обновления деятельности."""

    name: str | None = None
    parent_id: int | None = None


class ActivitySetMaxLevel(BaseModel):
    """Схема для установки максимального уровня вложенности деятельности."""

    name: str = Field(..., description="Название деятельности")
    max_level: int = Field(
        3, ge=1, le=10, description="Максимальный уровень вложенности"
    )
