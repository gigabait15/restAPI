from sqlalchemy import ARRAY, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.model import Base, BaseIDModel


class BuildingBase:
    """
    Базовый миксин с полями здания.

    Attributes:
        address: Адрес здания (до 255 символов).
        coordinates: Географические координаты [широта, долгота].
    """

    address: Mapped[str] = mapped_column(String(255), nullable=False)
    coordinates: Mapped[list[float]] = mapped_column(
        ARRAY(Float), nullable=False, default=[0.0, 0.0]
    )


class Building(BaseIDModel, BuildingBase, Base):
    """
    Модель здания.

    Содержит адрес и координаты здания.
    Организации связываются со зданиями через building_id.
    """

    __tablename__ = "buildings"

    organizations = relationship(
        "Organization", back_populates="building", lazy="select"
    )
