from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.education_level import EducationLevel
    from app.models.resume import Resume


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    education_level_id: Mapped[int] = mapped_column(ForeignKey("education_levels.id"))
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    institution: Mapped[str] = mapped_column(String(120), nullable=False)
    graduation_year: Mapped[date] = mapped_column(Date(), nullable=False)
    specialty_name: Mapped[str] = mapped_column(String(140), nullable=False)

    education_level: Mapped["EducationLevel"] = relationship("EducationLevel", back_populates="education")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="education")
