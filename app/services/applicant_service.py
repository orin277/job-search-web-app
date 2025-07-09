from typing import List

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

        applicant.user.name = applicant_data.name
        applicant.user.surname = applicant_data.surname
        applicant.user.email = applicant_data.email
        applicant.user.hashed_password = applicant_data.hashed_password

        applicant = await self.applicant_repo.update(applicant)
        return ApplicantRead.model_validate(applicant)
    
    async def delete(self, id: int) -> None:
        applicant = await self.applicant_repo.get_by_id(id)
        await self.applicant_repo.delete(applicant)

    async def gel_all(self, filter: ApplicantFilter) -> List[ApplicantRead]:
        applicant_models = await self.applicant_repo.get_all(filter.name, filter.surname)
        return [ApplicantRead.model_validate(model) for model in applicant_models]
    
