from fastapi import FastAPI

from app.models import *

from app.api.v1.applicants import router as router_applicants



app = FastAPI()

app.include_router(router_applicants)