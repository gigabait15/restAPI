from sqlalchemy import CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.model import Base, BaseIDModel


class ActivityBase:
    """
    Базовый миксин с полями деятельности.

    Attributes:
        name: Название деятельности (до 100 символов).
        parent_id: ID родительской деятельности (для иерархии).
        level: Максимальный уровень вложенности (по умолчанию 2).
    """

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("activities.id"), nullable=True, index=True
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, default=2)


class Activity(BaseIDModel, ActivityBase, Base):
    """
    Модель деятельности (вида деятельности организации).

    Поддерживает иерархическую структуру через связь parent-children.
    Организации связываются с деятельностями через activity_id.
    """

    __tablename__ = "activities"
    __table_args__ = (CheckConstraint("level >= 1", name="ck_activity_level_positive"),)

    parent = relationship(
        "Activity",
        remote_side="Activity.id",
        back_populates="children",
        lazy="select",
    )

    children = relationship(
        "Activity",
        back_populates="parent",
        lazy="select",
    )

    organizations = relationship(
        "Organization", back_populates="activity", lazy="select"
    )
