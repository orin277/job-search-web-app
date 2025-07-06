from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base

from app.core.config import settings

engine = create_async_engine(settings.db_url)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

def get_db_connection():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })