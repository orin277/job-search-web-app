from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

from app.models.resume_city import resume_city
from app.models.resume_employment_type import resume_employment_type
from app.models.resume_professional_field import resume_professional_field
from app.models.resume_work_location_type import resume_work_location_type


if TYPE_CHECKING:
    from app.models.applicant import Applicant
    from app.models.education import Education
    from app.models.employment_type import EmploymentType
    from app.models.work_location_type import WorkLocationType
    from app.models.professional_field import ProfessionalField
    from app.models.city import City
    from app.models.response import Response
    from app.models.candidate_skill import CandidateSkill
    from app.models.work_experience import WorkExperience


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    applicant_id: Mapped[int] = mapped_column(ForeignKey("applicants.id"))

    position: Mapped[str] = mapped_column(String(60), nullable=False)
    salary: Mapped[int] = mapped_column(Integer(), nullable=True)
    about_myself: Mapped[str] = mapped_column(String(1000), nullable=False)
    publication_date: Mapped[date] = mapped_column(Date(), nullable=False)

    applicant: Mapped["Applicant"] = relationship("Applicant", back_populates="resumes")
    candidate_skills: Mapped[List["CandidateSkill"]] = relationship("CandidateSkill", back_populates="resume")
    education: Mapped[List["Education"]] = relationship("Education", back_populates="resume")
    work_experience: Mapped[List["WorkExperience"]] = relationship("WorkExperience", back_populates="resume")
    responses: Mapped[List["Response"]] = relationship("Response", back_populates="resume")

    employment_types: Mapped[List["EmploymentType"]] = relationship(
        "EmploymentType",
        secondary=resume_employment_type,
        back_populates="resumes"
    )

    work_location_types: Mapped[List["WorkLocationType"]] = relationship(
        "WorkLocationType",
        secondary=resume_work_location_type,
        back_populates="resumes"
    )

    professional_fields: Mapped[List["ProfessionalField"]] = relationship(
        "ProfessionalField",
        secondary=resume_professional_field,
        back_populates="resumes"
    )

    cities: Mapped[List["City"]] = relationship(
        "City",
        secondary=resume_city,
        back_populates="resumes"
    )
