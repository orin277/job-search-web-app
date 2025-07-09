from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db_connection
from app.repositories.applicant_repo import ApplicantRepository, SqlAlchemyApplicantRepository
from app.services.applicant_service import ApplicantService


def get_applicant_repository(
    session: Session = Depends(get_db_connection)
) -> ApplicantRepository:
    return SqlAlchemyApplicantRepository(session)


def get_applicant_service(
    repo: ApplicantRepository = Depends(get_applicant_repository)
) -> ApplicantService:
    return ApplicantService(repo)