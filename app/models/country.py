from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.region import Region


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    regions: Mapped[List["Region"]] = relationship("Region", back_populates="country")
