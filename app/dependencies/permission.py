from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db_connection
from app.repositories.permission_repo import SqlAlchemyPermissionRepository, PermissionRepository
from app.services.permission_service import PermissionService


def get_permission_repository(
    session: Session = Depends(get_db_connection)
) -> PermissionRepository:
    return SqlAlchemyPermissionRepository(session)


def get_permission_service(
    repo: PermissionRepository = Depends(get_permission_repository)
) -> PermissionService:
    return PermissionService(repo)