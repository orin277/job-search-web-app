from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_role import UserRole

class UserRoleRepository(Protocol):
    async def get_by_id(self, id: int) -> UserRole | None:
        ...
    

class SqlAlchemyUserRoleRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def get_by_id(self, id: int) -> UserRole | None:
        query = (
            select(UserRole)
            .filter(UserRole.id==id)
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    