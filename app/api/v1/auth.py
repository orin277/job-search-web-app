from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import get_auth_service
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.utils.auth import get_client_ip


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    user_agent = request.headers.get("user-agent")
    ip_address = get_client_ip(request)
    return await auth_service.login(
        form_data.username, 
        form_data.password,
        user_agent,
        ip_address
    )