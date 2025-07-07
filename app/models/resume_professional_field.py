from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

resume_professional_field = Table(
    "resumes_professional_fields",
    Base.metadata,
    Column("resume_id", ForeignKey("resumes.id"), primary_key=True),
    Column("professional_field_id", ForeignKey("professional_fields.id"), primary_key=True)
)