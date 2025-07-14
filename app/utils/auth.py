import bcrypt
import jwt 
from datetime import datetime, timedelta, timezone

from app.core.config import settings



def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password=plain_password, 
                          hashed_password=hashed_password)


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})

    return jwt.encode(data, 
                    key=settings.auth.SECRET_KEY, 
                    algorithm=settings.auth.ALGORITHM
    )