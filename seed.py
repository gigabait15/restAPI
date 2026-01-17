"""
Скрипт для заполнения базы данных тестовыми данными.

Создаёт здания, деятельности (с иерархией) и организации.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.activity.model import Activity
from app.building.model import Building
from app.organization.model import Organization
from core.base.logger import get_logger
from core.database.model import Base
from core.database.session import async_session_maker, engine

logger = get_logger(__name__)


BUILDINGS_DATA: list[dict[str, Any]] = [
    {
        "address": "г. Москва, ул. Тверская, д. 1",
        "coordinates": [55.757718, 37.612276],
    },
    {
        "address": "г. Москва, ул. Арбат, д. 10",
        "coordinates": [55.752023, 37.591094],
    },
    {
        "address": "г. Москва, Красная площадь, д. 3",
        "coordinates": [55.753544, 37.621202],
    },
    {
        "address": "г. Москва, ул. Новый Арбат, д. 15",
        "coordinates": [55.752675, 37.583894],
    },
    {
        "address": "г. Москва, Ленинский проспект, д. 45",
        "coordinates": [55.703636, 37.587152],
    },
    {
        "address": "г. Санкт-Петербург, Невский проспект, д. 28",
        "coordinates": [59.935241, 30.327894],
    },
    {
        "address": "г. Санкт-Петербург, ул. Большая Морская, д. 18",
        "coordinates": [59.933861, 30.309118],
    },
    {
        "address": "г. Новосибирск, ул. Ленина, д. 1",
        "coordinates": [55.030199, 82.920430],
    },
]

ACTIVITIES_DATA: list[dict[str, Any]] = [
    {"name": "Еда", "parent_idx": None, "level": 3},
    {"name": "Автомобили", "parent_idx": None, "level": 3},
    {"name": "Услуги", "parent_idx": None, "level": 2},
    {"name": "Медицина", "parent_idx": None, "level": 3},
    {"name": "Мясная продукция", "parent_idx": 0, "level": 2},
    {"name": "Молочная продукция", "parent_idx": 0, "level": 2},
    {"name": "Выпечка", "parent_idx": 0, "level": 2},
    {"name": "Напитки", "parent_idx": 0, "level": 2},
    {"name": "Грузовые", "parent_idx": 1, "level": 2},
    {"name": "Легковые", "parent_idx": 1, "level": 2},
    {"name": "Запчасти", "parent_idx": 9, "level": 1},
    {"name": "Аксессуары", "parent_idx": 9, "level": 1},
    {"name": "Шины и диски", "parent_idx": 9, "level": 1},
    {"name": "Ремонт техники", "parent_idx": 2, "level": 1},
    {"name": "Клининг", "parent_idx": 2, "level": 1},
    {"name": "Стоматология", "parent_idx": 3, "level": 2},
    {"name": "Терапия", "parent_idx": 3, "level": 2},
    {"name": "Аптеки", "parent_idx": 3, "level": 1},
    {"name": "Колбасы", "parent_idx": 4, "level": 1},
    {"name": "Полуфабрикаты", "parent_idx": 4, "level": 1},
]


ORGANIZATIONS_DATA: list[dict[str, Any]] = [
    {
        "name": 'ООО "Рога и Копыта"',
        "phone_number": ["8-495-123-45-67", "8-495-123-45-68"],
        "building_idx": 0,
        "activity_idx": 4,
    },
    {
        "name": 'ООО "Молочный рай"',
        "phone_number": ["8-495-222-33-44"],
        "building_idx": 0,
        "activity_idx": 5,
    },
    {
        "name": 'АО "АвтоМир"',
        "phone_number": ["8-495-333-44-55", "8-800-100-200-300"],
        "building_idx": 1,
        "activity_idx": 9,
    },
    {
        "name": "ИП Петров - Шиномонтаж",
        "phone_number": ["8-926-555-66-77"],
        "building_idx": 1,
        "activity_idx": 12,
    },
    {
        "name": 'Клиника "Здоровье"',
        "phone_number": ["8-495-444-55-66", "8-495-444-55-67"],
        "building_idx": 2,
        "activity_idx": 15,
    },
    {
        "name": 'Пекарня "Хлебный дом"',
        "phone_number": ["8-495-666-77-88"],
        "building_idx": 3,
        "activity_idx": 6,
    },
    {
        "name": 'ООО "Чистый дом"',
        "phone_number": ["8-495-777-88-99", "8-495-777-88-00"],
        "building_idx": 4,
        "activity_idx": 14,
    },
    {
        "name": 'Аптека "Здравие"',
        "phone_number": ["8-812-111-22-33"],
        "building_idx": 5,
        "activity_idx": 17,
    },
    {
        "name": 'ООО "СевероЗапад Авто"',
        "phone_number": ["8-812-222-33-44", "8-812-222-33-45"],
        "building_idx": 6,
        "activity_idx": 8,
    },
    {
        "name": 'Кафе "Сибирские просторы"',
        "phone_number": ["8-383-333-44-55"],
        "building_idx": 7,
        "activity_idx": 0,
    },
    {
        "name": 'Магазин "Колбасный рай"',
        "phone_number": ["8-495-888-99-00"],
        "building_idx": 3,
        "activity_idx": 19,
    },
    {
        "name": 'ООО "Запчасти Люкс"',
        "phone_number": ["8-495-999-00-11", "8-800-555-35-35"],
        "building_idx": 4,
        "activity_idx": 10,
    },
]


async def seed_database(session: AsyncSession) -> dict[str, int]:
    """
    Заполняет базу данных тестовыми данными.

    Создаёт здания, деятельности и организации.

    Args:
        session: Асинхронная сессия базы данных.

    Returns:
        dict[str, int]: Словарь с количеством созданных записей по типам.
    """
    created_counts = {"buildings": 0, "activities": 0, "organizations": 0}

    logger.info("Создание зданий...")
    buildings = []
    for data in BUILDINGS_DATA:
        building = Building(
            address=data["address"],
            coordinates=data["coordinates"],
        )
        session.add(building)
        buildings.append(building)

    await session.flush()
    created_counts["buildings"] = len(buildings)
    logger.info(f"Создано зданий: {len(buildings)}")

    logger.info("Создание деятельностей...")
    activities: list[Activity] = [None] * len(ACTIVITIES_DATA)  # type: ignore

    for idx, data in enumerate(ACTIVITIES_DATA):
        if data["parent_idx"] is None:
            activity = Activity(
                name=data["name"],
                parent_id=None,
                level=data["level"],
            )
            session.add(activity)
            activities[idx] = activity

    await session.flush()

    created_in_pass = True
    while created_in_pass:
        created_in_pass = False
        for idx, data in enumerate(ACTIVITIES_DATA):
            if activities[idx] is not None:
                continue

            parent_idx = data["parent_idx"]
            if parent_idx is not None and activities[parent_idx] is not None:
                activity = Activity(
                    name=data["name"],
                    parent_id=activities[parent_idx].id,
                    level=data["level"],
                )
                session.add(activity)
                activities[idx] = activity
                created_in_pass = True

        if created_in_pass:
            await session.flush()

    created_counts["activities"] = len([a for a in activities if a is not None])
    logger.info(f"Создано деятельностей: {created_counts['activities']}")

    logger.info("Создание организаций...")
    organizations = []
    for data in ORGANIZATIONS_DATA:
        building_idx: int = data["building_idx"]
        activity_idx: int = data["activity_idx"]
        org = Organization(
            name=data["name"],
            phone_number=data["phone_number"],
            building_id=buildings[building_idx].id,
            activity_id=activities[activity_idx].id,  # type: ignore[union-attr]
        )
        session.add(org)
        organizations.append(org)

    await session.flush()
    created_counts["organizations"] = len(organizations)
    logger.info(f"Создано организаций: {len(organizations)}")

    await session.commit()
    logger.info("Данные успешно сохранены в БД")

    return created_counts


async def clear_database(session: AsyncSession) -> None:
    """
    Очищает все данные из таблиц (в правильном порядке из-за FK).

    Args:
        session: Асинхронная сессия базы данных.
    """
    logger.info("Очистка базы данных...")

    await session.execute(Organization.__table__.delete())
    await session.execute(Activity.__table__.delete())
    await session.execute(Building.__table__.delete())

    await session.commit()
    logger.info("База данных очищена")


async def ensure_schema() -> None:
    """
    Гарантирует наличие таблиц в БД перед сидинговыми операциями.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main() -> None:
    """Главная функция для запуска сидинга."""
    await ensure_schema()
    async with async_session_maker() as session:
        await clear_database(session)

        counts = await seed_database(session)

        print("\n" + "=" * 50)
        print("База данных успешно заполнена!")
        print("=" * 50)
        print(f"  Здания:       {counts['buildings']}")
        print(f"  Деятельности: {counts['activities']}")
        print(f"  Организации:  {counts['organizations']}")
        print("=" * 50 + "\n")
