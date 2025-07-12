from fastapi import Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base

import redis.asyncio as redis

from app.core.config import settings

engine = create_async_engine(settings.db_url)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_connection():
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()

async def get_redis_client():
    redis_client = redis.from_url(settings.redis_db_url)
    try:
        await redis_client.ping()
        print("Redis is connected")
    except Exception as e:
        print(f"Redis is not connected {e}")
    return redis_client

async def get_redis_db(request: Request):
    return request.app.state.redis_client


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })