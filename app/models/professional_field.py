from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class ProfessionalField(Base):
    __tablename__ = "professional_fields"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)