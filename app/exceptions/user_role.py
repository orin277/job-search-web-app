

from fastapi import HTTPException, status


class UserRoleNotFoundException(HTTPException):
    def __init__(self, user_role_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User role with id {user_role_id} not found"
        )