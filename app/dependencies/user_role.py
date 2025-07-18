from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db_connection
from app.repositories.user_role_repo import UserRoleRepository, SqlAlchemyUserRoleRepository


def get_user_role_repository(
    session: Session = Depends(get_db_connection)
) -> UserRoleRepository:
    return SqlAlchemyUserRoleRepository(session)