from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.response import Response


class ResponseStatus(Base):
    __tablename__ = "response_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

    responses: Mapped[List["Response"]] = relationship("Response", back_populates="response_status")