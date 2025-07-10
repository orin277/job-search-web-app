from fastapi import FastAPI

from app.models import *

from app.api.v1.applicants import router as router_applicants
from app.api.v1.interview import router as router_interview



app = FastAPI()

app.include_router(router_applicants)
app.include_router(router_interview)