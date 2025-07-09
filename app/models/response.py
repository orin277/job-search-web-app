from datetime import date
from typing import TYPE_CHECKING, List
from sqlalchemy import Column, Date, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


if TYPE_CHECKING:
    from app.models.resume import Resume
    from app.models.vacancy import Vacancy
    from app.models.response_status import ResponseStatus


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    response_status_id: Mapped[int] = mapped_column(ForeignKey("response_statuses.id"))

    cover_letter: Mapped[str] = mapped_column(String(500), nullable=True)
    employer_response: Mapped[str] = mapped_column(String(500), nullable=True)
    employer_response_date: Mapped[date] = mapped_column(Date(), nullable=True)
    applicant_response_date: Mapped[date] = mapped_column(Date(), nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="responses")
    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="responses")
    response_status: Mapped["ResponseStatus"] = relationship("ResponseStatus", back_populates="responses")