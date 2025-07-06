from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from job_search_web_app.db.database import Base

if TYPE_CHECKING:
    from job_search_web_app.models.user_type import UserType



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_types.id"))
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(40), nullable=False)
    user_type: Mapped["UserType"] = relationship("UserType", back_populates="users")
