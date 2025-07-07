from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

resume_work_location_type = Table(
    "resumes_work_location_types",
    Base.metadata,
    Column("resume_id", ForeignKey("resumes.id"), primary_key=True),
    Column("work_location_type_id", ForeignKey("work_location_types.id"), primary_key=True)
)