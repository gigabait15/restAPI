from app.building.model import Building
from app.building.schema import BuildingCreate, BuildingUpdate
from core.database.crud import CRUDBase


class CRUDBuilding(CRUDBase[Building, BuildingCreate, BuildingUpdate]):
    """CRUD операции для работы со зданиями (Building)."""
    pass


building = CRUDBuilding(Building)
