from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from job_search_web_app.db.database import Base

if TYPE_CHECKING:
    from job_search_web_app.models.user import User


class UserType(Base):
    __tablename__ = "user_types"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    users: Mapped[List["User"]] = relationship("User", back_populates="user_type")
