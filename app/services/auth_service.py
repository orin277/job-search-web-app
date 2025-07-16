from app.exceptions.auth import InvalidCredentialsException, RefreshTokenAlreadyExistsException, UserNotFoundException
from app.exceptions.exceptions import UniqueConstraintException
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.repositories.user_repo import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserRead
from app.utils.auth import create_access_token, create_refresh_token, verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository, refresh_token_repo: RefreshTokenRepository):
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if user is None or verify_password(password, user.hashed_password) == False:
            return None
        
        return user
    
    async def login(
            self, 
            email, 
            password,
            user_agent,
            ip_address
        ) -> Token:
        user = await self.authenticate_user(email, password)
        if user is None:
            raise InvalidCredentialsException()

        access_token = create_access_token({"sub": user.id})
        refresh_token, expiry_date = create_refresh_token({"sub": user.id})

        refresh_token_model = RefreshToken()
        refresh_token_model.token = refresh_token
        refresh_token_model.user_id = user.id
        refresh_token_model.user_agent = user_agent
        refresh_token_model.ip_address = ip_address
        refresh_token_model.expires_at = expiry_date.replace(tzinfo=None)

        try:
            await self.refresh_token_repo.create(refresh_token_model)
            return Token(
                access_token=access_token, 
                refresh_token=refresh_token,
                token_type="bearer"
            )
        except UniqueConstraintException as e:
            raise RefreshTokenAlreadyExistsException(e.field)
        
    async def get_user_by_id(self, id: int) -> UserRead:
        user = await self.user_repo.get_by_id(id)
        if user is None:
            raise UserNotFoundException()
        return UserRead.model_validate(user)

        

        