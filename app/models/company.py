from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.vacancy import Vacancy
    from app.models.professional_field import ProfessionalField
    from app.models.city import City


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    professional_field_id: Mapped[int] = mapped_column(ForeignKey("professional_fields.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    website: Mapped[str] = mapped_column(String(100), nullable=True)
    min_number_of_employees: Mapped[int] = mapped_column(Integer(), nullable=False)

    city: Mapped["City"] = relationship("City", back_populates="companies")
    professional_field: Mapped["ProfessionalField"] = relationship("ProfessionalField", back_populates="companies")
    vacancies: Mapped[List["Vacancy"]] = relationship("Vacancy", back_populates="company")
