from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.region import Region


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    region: Mapped["Region"] = relationship("Region", back_populates="cities")
    users: Mapped[List["User"]] = relationship("User", back_populates="city")
