from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models import resume_employment_type, vacancy_employment_type

if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.vacancy import Vacancy


class EmploymentType(Base):
    __tablename__ = "employment_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        secondary=resume_employment_type,
        back_populates="employment_types"
    )

    vacancies: Mapped[List["Vacancy"]] = relationship(
        "Vacancy",
        secondary=vacancy_employment_type,
        back_populates="employment_types"
    )
