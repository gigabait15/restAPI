from sqlalchemy import Float, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.activity.model import Activity
from app.building.model import Building
from app.organization.model import Organization
from app.organization.schema import OrganizationCreate, OrganizationUpdate
from core.base.config import EARTH_RADIUS_KM
from core.database.crud import CRUDBase


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):
    """CRUD операции для работы с организациями."""

    async def get_organizations_by_building_address(
        self, db: AsyncSession, building_address: str
    ) -> list[Organization]:
        """
        Получить список организаций по адресу здания.

        Args:
            db: Асинхронная сессия базы данных.
            building_address: Адрес здания для поиска.

        Returns:
            list[Organization]: Список организаций в указанном здании.
        """
        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(Building.address == building_address)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_organizations_by_activity_name(
        self, db: AsyncSession, activity_name: str
    ) -> list[Organization]:
        """
        Получить список организаций по названию вида деятельности.

        Args:
            db: Асинхронная сессия базы данных.
            activity_name: Название вида деятельности.

        Returns:
            list[Organization]: Список организаций с указанным видом деятельности.
        """
        stmt = (
            select(Organization)
            .join(Activity, Organization.activity_id == Activity.id)
            .where(Activity.name == activity_name)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_organizations_by_activity_with_children(
        self, db: AsyncSession, activity_name: str
    ) -> list[Organization]:
        """
        Получить организации по виду деятельности и всем дочерним видам.

        Использует рекурсивный CTE запрос для получения всех потомков указанной
        деятельности в иерархии.

        Например: "Еда" → организации с Еда, Мясная продукция, Молочная продукция.

        Args:
            db: Асинхронная сессия базы данных.
            activity_name: Название корневого вида деятельности.

        Returns:
            list[Organization]: Список организаций с указанным видом деятельности и дочерними.
        """
        activity_cte = (
            select(Activity.id)
            .where(Activity.name == activity_name)
            .cte(name="activity_tree", recursive=True)
        )

        activity_recursive = select(Activity.id).where(
            Activity.parent_id == activity_cte.c.id
        )

        activity_cte = activity_cte.union_all(activity_recursive)

        stmt = select(Organization).where(
            Organization.activity_id.in_(select(activity_cte.c.id))
        )

        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_organization_by_name(
        self, db: AsyncSession, name: str
    ) -> Organization | None:
        """
        Получить организацию по её названию.

        Args:
            db: Асинхронная сессия базы данных.
            name: Название организации.

        Returns:
            Organization | None: Найденная организация или None.
        """
        stmt = select(Organization).where(Organization.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_organizations_in_radius(
        self,
        db: AsyncSession,
        lat: float,
        lon: float,
        radius_km: float,
    ) -> list[Organization]:
        """
        Получить организации в радиусе от указанной точки.

        Использует формулу Haversine для вычисления расстояния между
        координатами точки и координатами зданий организаций.

        Args:
            db: Асинхронная сессия базы данных.
            lat: Широта центральной точки.
            lon: Долгота центральной точки.
            radius_km: Радиус поиска в километрах.

        Returns:
            list[Organization]: Список организаций в указанном радиусе.
        """
        lat_rad = func.radians(lat)
        lon_rad = func.radians(lon)
        building_lat_rad = func.radians(Building.coordinates[1].cast(Float))
        building_lon_rad = func.radians(Building.coordinates[2].cast(Float))

        dlat = building_lat_rad - lat_rad
        dlon = building_lon_rad - lon_rad

        a = func.power(func.sin(dlat / 2), 2) + func.cos(lat_rad) * func.cos(
            building_lat_rad
        ) * func.power(func.sin(dlon / 2), 2)
        c = 2 * func.atan2(func.sqrt(a), func.sqrt(1 - a))
        distance = EARTH_RADIUS_KM * c

        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(distance <= radius_km)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_organizations_in_bounds(
        self,
        db: AsyncSession,
        min_lat: float,
        min_lon: float,
        max_lat: float,
        max_lon: float,
    ) -> list[Organization]:
        """
        Получить организации в прямоугольной географической области.

        Фильтрует организации по координатам зданий, попадающим в указанный
        прямоугольник (bounding box).

        Args:
            db: Асинхронная сессия базы данных.
            min_lat: Минимальная широта (южная граница).
            min_lon: Минимальная долгота (западная граница).
            max_lat: Максимальная широта (северная граница).
            max_lon: Максимальная долгота (восточная граница).

        Returns:
            list[Organization]: Список организаций в указанной области.
        """
        building_lat = Building.coordinates[1].cast(Float)
        building_lon = Building.coordinates[2].cast(Float)

        stmt = (
            select(Organization)
            .join(Building, Organization.building_id == Building.id)
            .where(
                building_lat >= min_lat,
                building_lat <= max_lat,
                building_lon >= min_lon,
                building_lon <= max_lon,
            )
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())


organization = CRUDOrganization(Organization)
