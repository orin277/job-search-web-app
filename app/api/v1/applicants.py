from typing import Annotated, List
from fastapi import APIRouter, Depends, Query

from app.dependencies.applicant import get_applicant_service
from app.schemas.applicant import ApplicantCreate, ApplicantEdit, ApplicantFilter, ApplicantRead
from app.services.applicant_service import ApplicantService


router = APIRouter(
    prefix="/applicants",
    tags=["Applicants"]
)


@router.get("")
async def get_applicants(
    filter: Annotated[ApplicantFilter, Query()],
    applicant_service: ApplicantService = Depends(get_applicant_service)
) -> List[ApplicantRead]:
    return await applicant_service.gel_all(filter)


@router.post("")
async def create_applicant(
    applicant_data: Annotated[ApplicantCreate, Depends()],
    applicant_service: ApplicantService = Depends(get_applicant_service)
) -> ApplicantRead:
    applicant = await applicant_service.create(applicant_data)
    return applicant


@router.patch("/{id}")
async def update_applicant(
    applicant_data: Annotated[ApplicantEdit, Depends()],
    applicant_service: ApplicantService = Depends(get_applicant_service)
) -> ApplicantRead:
    applicant = await applicant_service.update(applicant_data)
    return applicant

@router.delete("/{id}")
async def delete_applicant(
    id: int,
    applicant_service: ApplicantService = Depends(get_applicant_service)
) -> None:
    applicant = await applicant_service.delete(id)
    return applicant