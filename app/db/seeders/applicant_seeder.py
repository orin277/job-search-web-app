from typing import List
from app.models.user import User
from app.dependencies.applicant import get_applicant_repository
from app.models.applicant import Applicant
from app.repositories.applicant_repo import ApplicantRepository



class ApplicantSeeder:
    def __init__(
        self,
        applicant_repo: ApplicantRepository
    ):
        self.applicant_repo = applicant_repo
        

    async def run(self, users: List[User]):
        applicants = []
        for i in range(len(users)):
            applicant = Applicant()
            applicant.user = users[i]
            applicants.append(applicant)
        await self.applicant_repo.create_many(applicants)


    @staticmethod
    def create_seeder(session):
        applicant_repo = get_applicant_repository(session)
        return ApplicantSeeder(applicant_repo)