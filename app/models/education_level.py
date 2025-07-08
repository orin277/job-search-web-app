from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.education import Education
    from app.models.vacancy import Vacancy


class EducationLevel(Base):
    __tablename__ = "education_levels"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    education: Mapped[List["Education"]] = relationship("Education", back_populates="education_level")
    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", back_populates="education_level")
