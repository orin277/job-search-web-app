from typing import TYPE_CHECKING, List
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.user_role_permission import user_role_permission

if TYPE_CHECKING:
    from app.models.user_role import UserRole


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    user_roles: Mapped[List["UserRole"]] = relationship(
        "UserRole",
        secondary=user_role_permission,
        back_populates="permissions"
    )