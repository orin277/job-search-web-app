

from fastapi import HTTPException, status


class PermissionNotFoundException(HTTPException):
    def __init__(self, permission_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permission with id {permission_id} not found"
        )

class PermissionAlreadyExistsException(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Permission with this {name} already exists"
        )