import bcrypt
from fastapi import Request
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


def create_token(data: dict, expiry_date: timedelta) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expiry_date})

    return jwt.encode(to_encode, 
                    key=settings.auth.SECRET_KEY, 
                    algorithm=settings.auth.ALGORITHM
    )


def create_access_token(data: dict) -> str:
    expiry_date = datetime.now(timezone.utc) + timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expiry_date)

def create_refresh_token(data: dict) -> str:
    expiry_date = datetime.now(timezone.utc) + timedelta(days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(data, expiry_date), expiry_date


def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host