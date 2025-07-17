from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

user_role_permission = Table(
    "user_roles_permissions",
    Base.metadata,
    Column("user_role_id", ForeignKey("user_roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True)
)