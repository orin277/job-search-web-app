from typing import TYPE_CHECKING
from datetime import date, datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    user_agent: Mapped[str] = mapped_column(String(512), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now(timezone.utc).replace(tzinfo=None))
    expires_at: Mapped[datetime] = mapped_column(DateTime())

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
