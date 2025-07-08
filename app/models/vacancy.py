from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Boolean, Column, Date, ForeignKey, String, Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


if TYPE_CHECKING:
    from app.models.employer import Employer
    from app.models.company import Company
    from app.models.response import Response



class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))

    position: Mapped[str] = mapped_column(String(60), nullable=False)
    min_salary: Mapped[int] = mapped_column(Integer(), nullable=True)
    max_salary: Mapped[int] = mapped_column(Integer(), nullable=True)
    min_experience: Mapped[int] = mapped_column(SmallInteger(), nullable=False, default=0)
    description: Mapped[str] = mapped_column(String(3000), nullable=True)
    publication_date: Mapped[date] = mapped_column(Date(), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

    employer: Mapped["Employer"] = relationship("Employer", back_populates="vacancies")
    company: Mapped["Company"] = relationship("Company", back_populates="vacancies")
    responses: Mapped[List["Response"]] = relationship("Response", back_populates="vacancy")