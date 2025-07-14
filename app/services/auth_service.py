


from app.exceptions.auth import InvalidCredentialsException
from app.repositories.user_repo import UserRepository
from app.schemas.auth import Token
from app.utils.auth import create_access_token, verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if user is None or verify_password(password, user.hashed_password) == False:
            return None
        
        return user
    
    async def login(self, email, password) -> Token:
        print(email, password)
        user = await self.authenticate_user(email, password)
        if user is None:
            raise InvalidCredentialsException()

        access_token = create_access_token({"sub": user.id})

        return Token(
            access_token=access_token, token_type="bearer"
        )