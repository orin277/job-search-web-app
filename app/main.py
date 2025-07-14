from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.database import get_redis_client
from app.models import *

from app.api.v1.applicants import router as router_applicants
from app.api.v1.interview import router as router_interview
from app.api.v1.auth import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_client = await get_redis_client()
    yield
    await app.state.redis_client.close()


app = FastAPI(lifespan=lifespan)


app.include_router(router_applicants)
app.include_router(router_interview)
app.include_router(router_auth)