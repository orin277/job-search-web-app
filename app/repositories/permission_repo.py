from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import UniqueConstraintException
from app.models.user_role_permission import user_role_permission
from app.models.permission import Permission
from app.models.user import User
from app.models.user_role import UserRole

class PermissionRepository(Protocol):
    async def create(self, permission: Permission) -> Permission:
        ...

    async def update(self, permission: Permission) -> Permission:
        ...

    async def delete(self, permission: Permission) -> None:
        ...

    async def get_by_user_role_id(
        self, 
        user_role_id: int
    ) -> List[Permission]:
        ...

    async def get_by_id(self, id: int) -> Permission | None:
        ...

    async def add_user_role(self, permission: Permission, user_role: UserRole) -> None:
        ...

    async def delete_user_role(self, permission: Permission, user_role: UserRole) -> None:
        ...


class SqlAlchemyPermissionRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, permission: Permission) -> Permission:
        try:
            self.session.add(permission)
            await self.session.commit()
            await self.session.refresh(permission)
            return permission
        except IntegrityError as e:
            await self.session.rollback()
            if "UNIQUE" in str(e.orig).upper():
                raise UniqueConstraintException("permission") from e
            raise

    
    async def update(self, permission: Permission) -> Permission:
        try:
            await self.session.commit()
            await self.session.refresh(permission)
            return permission
        except IntegrityError as e:
            await self.session.rollback()
            if "UNIQUE" in str(e.orig).upper():
                raise UniqueConstraintException("permission") from e
            raise
    
    async def delete(self, permission: Permission) -> None:
        await self.session.delete(permission)
        await self.session.commit()

    async def get_by_user_role_id(
        self,
        user_role_id: int
    ) -> List[str]:
        query = (
            select(Permission.name)
            .join(user_role_permission)
            .filter(user_role_permission.c.user_role_id == user_role_id)
        )

        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> Permission | None:
        query = (
            select(Permission)
            .filter(Permission.id==id)
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def add_user_role(self, permission: Permission, user_role: UserRole) -> None:
        if permission not in user_role.permissions:
            user_role.permissions.append(permission)
            await self.session.commit()

    async def delete_user_role(self, permission: Permission, user_role: UserRole) -> None:
        if permission in user_role.permissions:
            user_role.permissions.remove(permission)
            await self.session.commit()
    