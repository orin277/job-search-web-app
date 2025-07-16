from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.exceptions.auth import InvalidTokenException, TokenExpiredException

from app.db.database import get_db_connection
from app.dependencies.user import get_user_repository
from app.repositories.refresh_token_repo import RefreshTokenRepository, SqlAlchemyRefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_refresh_token_repository(
    session: Session = Depends(get_db_connection)
) -> RefreshTokenRepository:
    return SqlAlchemyRefreshTokenRepository(session)

def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    refresh_token_repo: UserRepository = Depends(get_refresh_token_repository)
) -> AuthService:
    return AuthService(user_repo, refresh_token_repo)


async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        id: int = payload.get("sub")
        if id is None:
            raise InvalidTokenException()
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.PyJWTError:
        raise InvalidTokenException()
    user = await auth_service.get_user_by_id(id)
    return user