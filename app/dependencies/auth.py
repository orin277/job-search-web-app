from fastapi import Depends

from app.dependencies.user import get_user_repository
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService



def get_auth_service(
    repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(repo)