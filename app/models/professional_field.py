from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models import resume_professional_field, vacancy_professional_field
from app.models.vacancy import Vacancy

if TYPE_CHECKING:
    from app.models.work_experience import WorkExperience
    from app.models.resume import Resume
    from app.models.company import Company


class ProfessionalField(Base):
    __tablename__ = "professional_fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    work_experience: Mapped[List["WorkExperience"]] = relationship("WorkExperience", back_populates="professional_field")
    companies: Mapped[List["Company"]] = relationship("Company", back_populates="professional_field")

    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        secondary=resume_professional_field,
        back_populates="professional_fields"
    )

    vacancies: Mapped[List["Vacancy"]] = relationship(
        "Vacancy",
        secondary=vacancy_professional_field,
        back_populates="professional_fields"
    )
