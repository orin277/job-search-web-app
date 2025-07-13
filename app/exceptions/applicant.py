

from fastapi import HTTPException, status


class ApplicantNotFoundException(HTTPException):
    def __init__(self, applicant_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Applicant with id {applicant_id} not found"
        )

class EmailAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with this {email} already exists"
        )