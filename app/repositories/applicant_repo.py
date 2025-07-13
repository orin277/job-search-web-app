from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, contains_eager

from app.models.applicant import Applicant
from app.models.user import User

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
        surname: str | None,
        email: str | None,
        phone: str | None,
        city_id: int | None
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
        surname: str | None,
        email: str | None,
        phone: str | None,
        city_id: int | None,
        offset: int | None,
        limit: int | None
    ) -> List[Applicant]:
        query = (
            select(Applicant)
            .join(User)
            .options(contains_eager(Applicant.user)
                     .load_only(User.id, User.user_type_id, User.name, 
                                User.surname, User.city_id, User.email, User.phone)
                     )
            )
        if name:
            query = query.filter(User.name.ilike(f'%{name}%'))
        if surname:
            query = query.filter(User.surname.ilike(f'%{surname}%'))
        if city_id:
            query = query.filter(User.city_id == city_id)
        if email:
            query = query.filter(User.email.ilike(f'%{email}%'))
        if phone:
            query = query.filter(User.phone.ilike(f'%{phone}%'))

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, id: int) -> Applicant | None:
        query = (
            select(Applicant)
            .options(joinedload(Applicant.user))
            .filter(Applicant.id==id)
        )
        
        result = await self.session.execute(query)
        return result.scalar_one_or_none()