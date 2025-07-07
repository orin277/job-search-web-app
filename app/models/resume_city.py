from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

resume_city = Table(
    "resumes_cities",
    Base.metadata,
    Column("resume_id", ForeignKey("resumes.id"), primary_key=True),
    Column("city_id", ForeignKey("cities.id"), primary_key=True)
)