from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.exceptions.exceptions import UniqueConstraintException
from app.models.refresh_token import RefreshToken

class RefreshTokenRepository(Protocol):
    async def create(self, applicant: RefreshToken) -> RefreshToken:
        ...

    async def update(self, applicant: RefreshToken) -> RefreshToken:
        ...

    async def delete(self, applicant: RefreshToken) -> None:
        ...

    async def get_by_token_name(self, token_name: str) -> RefreshToken | None:
        ...


class SqlAlchemyRefreshTokenRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, token: RefreshToken) -> RefreshToken:
        try:
            self.session.add(token)
            await self.session.commit()
            await self.session.refresh(token)
            return token
        except IntegrityError as e:
            await self.session.rollback()
            if "UNIQUE" in str(e.orig).upper():
                raise UniqueConstraintException("token") from e
            raise
    
    async def update(self, token: RefreshToken) -> RefreshToken:
        try:
            await self.session.commit()
            await self.session.refresh(token)
            return token
        except IntegrityError as e:
            await self.session.rollback()
            if "UNIQUE" in str(e.orig).upper():
                raise UniqueConstraintException("token") from e
            raise
    
    async def delete(self, token: RefreshToken) -> None:
        await self.session.delete(token)
        await self.session.commit()
    
    async def get_by_token_name(self, token_name: str) -> RefreshToken | None:
        query = select(RefreshToken).filter(RefreshToken.token==token_name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()