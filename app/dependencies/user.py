from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db_connection
from app.repositories.user_repo import SqlAlchemyUserRepository, UserRepository



def get_user_repository(
    session: Session = Depends(get_db_connection)
) -> UserRepository:
    return SqlAlchemyUserRepository(session)