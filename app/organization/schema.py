from pydantic import BaseModel, Field

from core.base.schema import BaseCreateSchema, BaseReadSchema, BaseUpdateSchema


class OrganizationCreate(BaseCreateSchema):
    """Схема для создания организации."""

    name: str
    phone_number: list[str]
    building_id: int
    activity_id: int


class OrganizationRead(BaseReadSchema):
    """Схема для чтения данных организации."""

    name: str
    phone_number: list[str]
    building_id: int
    activity_id: int


class OrganizationUpdate(BaseUpdateSchema):
    """Схема для обновления организации."""

    name: str | None = None
    phone_number: list[str] | None = None


class GeoRadiusQuery(BaseModel):
    """
    Схема запроса для поиска в радиусе от точки.

    Используется для геопоиска организаций в заданном радиусе
    от указанных координат.
    """

    lat: float = Field(..., description="Широта центра")
    lon: float = Field(..., description="Долгота центра")
    radius_km: float = Field(..., gt=0, description="Радиус в километрах")


class GeoBoundsQuery(BaseModel):
    """
    Схема запроса для поиска в прямоугольной области.

    Используется для геопоиска организаций в пределах
    заданного bounding box.
    """

    min_lat: float = Field(..., description="Минимальная широта")
    min_lon: float = Field(..., description="Минимальная долгота")
    max_lat: float = Field(..., description="Максимальная широта")
    max_lon: float = Field(..., description="Максимальная долгота")
