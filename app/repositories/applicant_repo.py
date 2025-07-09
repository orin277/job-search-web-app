from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.applicant import Applicant

class ApplicantRepository(Protocol):
    async def create(self, applicant: Applicant) -> Applicant:
        ...

    async def update(self, applicant: Applicant) -> Applicant:
        ...

    async def delete(self, applicant: Applicant) -> None:
        ...

    async def get_all(
        self, 
        name: str | None,
        surname: str | None
    ) -> List[Applicant]:
        ...

    async def get_by_id(self, id: int) -> Applicant | None:
        ...


class SqlAlchemyApplicantRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create(self, applicant: Applicant) -> Applicant:
        self.session.add(applicant)

        await self.session.commit()
        await self.session.refresh(applicant)
        
        return applicant
    
    async def update(self, applicant: Applicant) -> Applicant:
        await self.session.commit()
        await self.session.refresh(applicant)

        return applicant
    
    async def delete(self, applicant: Applicant) -> None:
        await self.session.delete(applicant)
        await self.session.commit()

    async def get_all(
        self,
        name: str | None,
        surname: str | None
    ) -> List[Applicant]:
        query = select(Applicant).options(joinedload(Applicant.user))
        if name:
            query = query.filter(Applicant.user.name == name)
        if surname:
            query = query.filter(Applicant.user.surname == surname)

        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> Applicant | None:
        query = select(Applicant).options(joinedload(Applicant.user)).filter(Applicant.id==id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()