from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions.exceptions import UniqueConstraintException
from app.models.user import User

class UserRepository(Protocol):
    async def get_by_id(self, id: int) -> User | None:
        ...
    
    async def get_by_email(self, email: str) -> User | None:
        ...


class SqlAlchemyUserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def get_by_id(self, id: int) -> User | None:
        query = (
            select(User)
            .filter(User.id==id)
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        query = (
            select(User)
            .filter(User.email==email)
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()