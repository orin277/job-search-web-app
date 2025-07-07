from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models import resume_city

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.region import Region
    from app.models.work_experience import WorkExperience
    from app.models.resume import Resume


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    region: Mapped["Region"] = relationship("Region", back_populates="cities")
    users: Mapped[List["User"]] = relationship("User", back_populates="city")
    work_experience: Mapped[List["WorkExperience"]] = relationship("WorkExperience", back_populates="city")

    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        secondary=resume_city,
        back_populates="cities"
    )
