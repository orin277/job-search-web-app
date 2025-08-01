from typing import TYPE_CHECKING, List
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.models.user_role_permission import user_role_permission

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.permission import Permission



class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    users: Mapped[List["User"]] = relationship("User", back_populates="user_role")

    permissions: Mapped[List["Permission"]] = relationship(
        "Permission",
        secondary=user_role_permission,
        back_populates="user_roles"
    )
