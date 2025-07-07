from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

resume_employment_type = Table(
    "resumes_employment_types",
    Base.metadata,
    Column("resume_id", ForeignKey("resumes.id"), primary_key=True),
    Column("employment_type_id", ForeignKey("employment_types.id"), primary_key=True)
)