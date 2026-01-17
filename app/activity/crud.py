from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.activity.model import Activity
from app.activity.schema import ActivityCreate, ActivityUpdate
from core.database.crud import CRUDBase


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    """CRUD операции для работы с деятельностями (Activity)."""

    async def get_by_name(self, db: AsyncSession, name: str) -> Activity | None:
        """
        Получить деятельность по названию.

        Args:
            db: Асинхронная сессия базы данных.
            name: Название деятельности для поиска.

        Returns:
            Activity | None: Найденная деятельность или None.
        """
        stmt = select(Activity).where(Activity.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def set_max_level_by_name(
        self,
        db: AsyncSession,
        name: str,
        max_level: int = 3,
    ) -> Activity | None:
        """
        Установить ограничение уровня вложенности для деятельности по названию.

        Деятельность и её потомки не смогут уходить глубже max_level в иерархии.

        Args:
            db: Асинхронная сессия базы данных.
            name: Название деятельности.
            max_level: Максимальный уровень вложенности (по умолчанию 3).

        Returns:
            Activity | None: Обновлённая деятельность или None если не найдена.
        """
        db_obj = await self.get_by_name(db, name)
        if db_obj is None:
            return None

        db_obj.level = max_level
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


activity = CRUDActivity(Activity)
