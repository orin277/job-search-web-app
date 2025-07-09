from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.resume_work_location_type import resume_work_location_type
from app.models.vacancy_work_location_type import vacancy_work_location_type


if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.vacancy import Vacancy


class WorkLocationType(Base):
    __tablename__ = "work_location_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    resumes: Mapped[List["Resume"]] = relationship(
        "Resume",
        secondary=resume_work_location_type,
        back_populates="work_location_types"
    )

    vacancies: Mapped[List["Vacancy"]] = relationship(
        "Vacancy",
        secondary=vacancy_work_location_type,
        back_populates="work_location_types"
    )
