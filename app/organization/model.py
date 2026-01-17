from sqlalchemy import ARRAY, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.model import Base, BaseIDModel


class OrganizationBase:
    """
    Базовый миксин с полями организации.

    Attributes:
        name: Название организации (уникальное, до 100 символов).
        phone_number: Список номеров телефонов.
        building_id: ID здания, в котором находится организация.
        activity_id: ID вида деятельности организации.
    """

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[list[str]] = mapped_column(ARRAY(String(50)), nullable=False)
    building_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("buildings.id"), nullable=False, index=True
    )
    activity_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("activities.id"), nullable=False, index=True
    )


class Organization(BaseIDModel, OrganizationBase, Base):
    """
    Модель организации.

    Представляет организацию с привязкой к зданию и виду деятельности.
    Содержит контактную информацию (телефоны).
    """

    __tablename__ = "organizations"

    building = relationship("Building", back_populates="organizations", lazy="select")
    activity = relationship("Activity", back_populates="organizations", lazy="select")
