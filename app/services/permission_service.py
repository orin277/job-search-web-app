from typing import List

from app.exceptions.exceptions import UniqueConstraintException
from app.exceptions.permission import PermissionAlreadyExistsException, PermissionNotFoundException
from app.exceptions.user_role import UserRoleNotFoundException
from app.models.permission import Permission
from app.repositories.permission_repo import PermissionRepository
from app.repositories.user_role_repo import UserRoleRepository
from app.schemas.permission import PermissionCreate, PermissionEdit, PermissionNameRead, PermissionRead



class PermissionService:
    def __init__(self, permission_repo: PermissionRepository, user_role_repo: UserRoleRepository):
        self.permission_repo = permission_repo
        self.user_role_repo = user_role_repo

    async def create(self, permission_data: PermissionCreate) -> PermissionRead:
        permission = Permission(
            name=permission_data.name
        )
        try:
            permission = await self.permission_repo.create(permission)
            return PermissionRead.model_validate(permission)
        except UniqueConstraintException as e:
            raise PermissionAlreadyExistsException(e.field)
        
    
    async def update(self, permission_data: PermissionEdit) -> PermissionRead:
        permission = await self.permission_repo.get_by_id(permission_data.id)
        if permission:
            for field, value in permission_data.model_dump(exclude_unset=True).items():
                setattr(permission, field, value)
        else:
            raise PermissionNotFoundException(permission_data.id)
        
        try:
            permission = await self.permission_repo.update(permission)
            return PermissionRead.model_validate(permission)
        except UniqueConstraintException as e:
            raise PermissionAlreadyExistsException(e.field)
        
    
    async def delete(self, id: int) -> None:
        permission = await self.permission_repo.get_by_id(id)
        if permission:
            await self.permission_repo.delete(permission)
        else:
            raise PermissionNotFoundException(id)

    async def gel_by_user_role(self, user_role_id: int) -> List[str]:
        permissions = await self.permission_repo.get_by_user_role_id(user_role_id)
        return permissions
    
    async def add_user_role(self, permission_id: int, user_role_id: int) -> None:
        permission = await self.permission_repo.get_by_id(permission_id)
        user_role = await self.user_role_repo.get_by_id(user_role_id)

        if permission is None:
            raise PermissionNotFoundException(permission_id)
        if user_role is None:
            raise UserRoleNotFoundException(user_role_id)

        self.permission_repo.add_user_role(permission, user_role)

    async def delete_user_role(self, permission_id: int, user_role_id: int) -> None:
        permission = await self.permission_repo.get_by_id(permission_id)
        user_role = await self.user_role_repo.get_by_id(user_role_id)

        if permission is None:
            raise PermissionNotFoundException(permission_id)
        if user_role is None:
            raise UserRoleNotFoundException(user_role_id)

        self.permission_repo.delete_user_role(permission, user_role)


    
