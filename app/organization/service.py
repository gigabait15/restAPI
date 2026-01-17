from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.organization.crud import organization
from app.organization.schema import OrganizationRead
from core.base.logger import get_logger
from core.database.session import get_async_session

logger = get_logger(__name__)


class OrganizationService:
    """Сервисный слой для работы с организациями."""

    def __init__(
        self,
        db_session: AsyncSession,
    ):
        """
        Инициализация сервиса организаций.

        Args:
            db_session: Асинхронная сессия базы данных.
        """
        self.crud = organization
        self.db_session = db_session

    async def get_organizations_by_building_address(
        self, building_address: str
    ) -> list[OrganizationRead]:
        """
        Получить список организаций по адресу здания.

        Args:
            building_address: Адрес здания для поиска.

        Returns:
            list[OrganizationRead]: Список организаций в указанном здании.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            objects = await self.crud.get_organizations_by_building_address(
                self.db_session, building_address
            )
        except Exception as e:
            logger.error(f"Error getting organizations by building address: {e}")
            raise Exception(f"Error getting organizations by building address: {e}")
        return [OrganizationRead.model_validate(obj) for obj in objects]

    async def get_organizations_by_activity_name(
        self, activity_name: str
    ) -> list[OrganizationRead]:
        """
        Получить список организаций по названию вида деятельности.

        Args:
            activity_name: Название вида деятельности.

        Returns:
            list[OrganizationRead]: Список организаций с указанным видом деятельности.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            objects = await self.crud.get_organizations_by_activity_name(
                self.db_session, activity_name
            )
        except Exception as e:
            logger.error(f"Error getting organizations by activity: {e}")
            raise Exception(f"Error getting organizations by activity: {e}")
        return [OrganizationRead.model_validate(obj) for obj in objects]

    async def get_organization_by_name(self, name: str) -> OrganizationRead | None:
        """
        Получить организацию по её названию.

        Args:
            name: Название организации для поиска.

        Returns:
            OrganizationRead | None: Данные организации или None если не найдена.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            object = await self.crud.get_organization_by_name(self.db_session, name)
        except Exception as e:
            logger.error(f"Error getting organization by name: {e}")
            raise Exception(f"Error getting organization by name: {e}")
        return OrganizationRead.model_validate(object) if object else None

    async def get_organizations_by_activity_with_children(
        self, activity_name: str
    ) -> list[OrganizationRead]:
        """
        Получить организации по виду деятельности и всем дочерним видам.

        Рекурсивно находит все дочерние виды деятельности и возвращает
        организации, относящиеся к любому из них.

        Args:
            activity_name: Название корневого вида деятельности.

        Returns:
            list[OrganizationRead]: Список организаций с указанной и дочерними деятельностями.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            objects = await self.crud.get_organizations_by_activity_with_children(
                self.db_session, activity_name
            )
        except Exception as e:
            logger.error(f"Error getting organizations by activity tree: {e}")
            raise Exception(f"Error getting organizations by activity tree: {e}")
        return [OrganizationRead.model_validate(obj) for obj in objects]

    async def get_organizations_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> list[OrganizationRead]:
        """
        Получить организации в радиусе от указанной географической точки.

        Args:
            lat: Широта центральной точки.
            lon: Долгота центральной точки.
            radius_km: Радиус поиска в километрах.

        Returns:
            list[OrganizationRead]: Список организаций в указанном радиусе.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            objects = await self.crud.get_organizations_in_radius(
                self.db_session, lat, lon, radius_km
            )
        except Exception as e:
            logger.error(f"Error getting organizations in radius: {e}")
            raise Exception(f"Error getting organizations in radius: {e}")
        return [OrganizationRead.model_validate(obj) for obj in objects]

    async def get_organizations_in_bounds(
        self, min_lat: float, min_lon: float, max_lat: float, max_lon: float
    ) -> list[OrganizationRead]:
        """
        Получить организации в прямоугольной географической области.

        Args:
            min_lat: Минимальная широта (южная граница).
            min_lon: Минимальная долгота (западная граница).
            max_lat: Максимальная широта (северная граница).
            max_lon: Максимальная долгота (восточная граница).

        Returns:
            list[OrganizationRead]: Список организаций в указанной области.

        Raises:
            Exception: При ошибке получения данных из БД.
        """
        try:
            objects = await self.crud.get_organizations_in_bounds(
                self.db_session, min_lat, min_lon, max_lat, max_lon
            )
        except Exception as e:
            logger.error(f"Error getting organizations in bounds: {e}")
            raise Exception(f"Error getting organizations in bounds: {e}")
        return [OrganizationRead.model_validate(obj) for obj in objects]


async def get_organization_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> OrganizationService:
    """
    Фабрика для создания экземпляра OrganizationService.

    Используется как dependency в FastAPI для внедрения сервиса.

    Args:
        db_session: Асинхронная сессия базы данных.

    Returns:
        OrganizationService: Экземпляр сервиса организаций.
    """
    return OrganizationService(db_session)
