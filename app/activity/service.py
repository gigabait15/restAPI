from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.activity.crud import activity
from app.activity.schema import ActivityRead
from core.base.logger import get_logger
from core.database.session import get_async_session

logger = get_logger(__name__)


class ActivityService:
    """Сервисный слой для работы с деятельностями (Activity)."""

    def __init__(self, db_session: AsyncSession):
        """
        Инициализация сервиса деятельностей.

        Args:
            db_session: Асинхронная сессия базы данных.
        """
        self.crud = activity
        self.db_session = db_session

    async def set_max_level_by_name(
        self, name: str, max_level: int = 3
    ) -> ActivityRead | None:
        """
        Установить ограничение уровня вложенности для деятельности по названию.

        Args:
            name: Название деятельности.
            max_level: Максимальный уровень вложенности (по умолчанию 3).

        Returns:
            ActivityRead | None: Обновлённые данные деятельности или None если не найдена.

        Raises:
            Exception: При ошибке обновления данных.
        """
        try:
            obj = await self.crud.set_max_level_by_name(
                self.db_session, name, max_level
            )
        except Exception as e:
            logger.error(f"Error setting max level for activity: {e}")
            raise Exception(f"Error setting max level for activity: {e}")
        return ActivityRead.model_validate(obj) if obj else None


async def get_activity_service(
    db_session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ActivityService:
    """
    Фабрика для создания экземпляра ActivityService.

    Используется как dependency в FastAPI для внедрения сервиса.

    Args:
        db_session: Асинхронная сессия базы данных.

    Returns:
        ActivityService: Экземпляр сервиса деятельностей.
    """
    return ActivityService(db_session)
