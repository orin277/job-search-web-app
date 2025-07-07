from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.education import Education
from app.models.eployment_type import EmploymentType
from app.models.professional_field import ProfessionalField

if TYPE_CHECKING:
    from app.models.applicant import Applicant


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))

    position: Mapped[str] = mapped_column(String(60), nullable=False)
    salary: Mapped[int] = mapped_column(Integer(), nullable=True)
    about_myself: Mapped[str] = mapped_column(String(1000), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date(), nullable=False)

    applicant: Mapped["Applicant"] = relationship("Applicant", back_populates="resumes")
