from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.country import Country
    from app.models.city import City


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"))
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    country: Mapped["Country"] = relationship("Country", back_populates="regions")
    cities: Mapped[List["City"]] = relationship("City", back_populates="region")
