from typing import List

from app.exceptions.applicant import ApplicantNotFoundException
from app.models.applicant import Applicant
from app.models.user import User
from app.repositories.applicant_repo import ApplicantRepository
from app.schemas.applicant import ApplicantCreate, ApplicantEdit, ApplicantFilter, ApplicantRead



class ApplicantService:
    def __init__(self, applicant_repo: ApplicantRepository):
        self.applicant_repo = applicant_repo

    async def create(self, applicant_data: ApplicantCreate) -> ApplicantRead:
        user = User(
            user_type_id=2,
            name=applicant_data.name,
            surname=applicant_data.surname,
            phone=applicant_data.phone,
            email=applicant_data.email,
            hashed_password=applicant_data.hashed_password
        )

        applicant = Applicant(
            user=user  
        )

        applicant = await self.applicant_repo.create(applicant)
        return ApplicantRead.model_validate(applicant)
    
    async def update(self, applicant_data: ApplicantEdit) -> ApplicantRead:
        applicant = await self.applicant_repo.get_by_id(applicant_data.id)
        if applicant:
            if applicant_data.user:
                for field, value in applicant_data.user.model_dump(exclude_unset=True).items():
                    setattr(applicant.user, field, value)

            for field, value in applicant_data.model_dump(exclude={"user"}, exclude_unset=True).items():
                setattr(applicant, field, value)
        else:
            raise ApplicantNotFoundException(applicant_data.id)

        applicant = await self.applicant_repo.update(applicant)
        return ApplicantRead.model_validate(applicant)
    
    async def delete(self, id: int) -> None:
        applicant = await self.applicant_repo.get_by_id(id)
        if applicant:
            await self.applicant_repo.delete(applicant)
        else:
            raise ApplicantNotFoundException(id)

    async def gel_all(self, filter: ApplicantFilter) -> List[ApplicantRead]:
        applicant_models = await self.applicant_repo.get_all(filter.name, filter.surname, 
                                                             filter.email, filter.phone, 
                                                             filter.city_id,
                                                             filter.offset, filter.limit)
        return [ApplicantRead.model_validate(model) for model in applicant_models]
    
