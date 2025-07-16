from fastapi import Depends
from pytest import Session

from app.db.database import get_db_connection
from app.dependencies.user import get_user_repository
from app.repositories.refresh_token_repo import RefreshTokenRepository, SqlAlchemyRefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService

def get_refresh_token_repository(
    session: Session = Depends(get_db_connection)
) -> RefreshTokenRepository:
    return SqlAlchemyRefreshTokenRepository(session)

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    refresh_token_repo: UserRepository = Depends(get_refresh_token_repository)
) -> AuthService:
    return AuthService(user_repo, refresh_token_repo)