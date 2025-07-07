from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.resume import Resume


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="candidate_skills")
