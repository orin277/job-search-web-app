from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.professional_field import ProfessionalField
    from app.models.city import City



class WorkExperience(Base):
    __tablename__ = "work_experience"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    professional_field_id: Mapped[int] = mapped_column(ForeignKey("professional_fields.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)

    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
    position_title: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date(), nullable=False)
    end_date: Mapped[date] = mapped_column(Date(), nullable=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="work_experience")
    professional_field: Mapped["ProfessionalField"] = relationship("ProfessionalField", back_populates="work_experience")
    city: Mapped["City"] = relationship("City", back_populates="work_experience")
