from core.base.schema import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema


class BuildingCreate(BaseCreateSchema):
    """Схема для создания здания."""

    address: str
    coordinates: list[float] = [0.0, 0.0]


class BuildingRead(BaseReadSchema):
    """Схема для чтения данных здания."""

    address: str
    coordinates: list[float]


class BuildingUpdate(BaseUpdateSchema):
    """Схема для обновления здания."""

    address: str | None = None
    coordinates: list[float] | None = None
