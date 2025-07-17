from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user_role import UserRole
    from app.models.applicant import Applicant
    from app.models.employer import Employer
    from app.models.city import City
    from app.models.refresh_token import RefreshToken


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_role_id: Mapped[int] = mapped_column(ForeignKey("user_roles.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=True)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(60), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(40), nullable=False)

    user_role: Mapped["UserRole"] = relationship("UserRole", back_populates="users")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    city: Mapped["City"] = relationship("City", back_populates="users")
    applicant: Mapped["Applicant | None"] = relationship("Applicant", back_populates="user")
    employer: Mapped["Employer | None"] = relationship("Employer", back_populates="user")
