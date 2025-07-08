from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

vacancy_professional_field = Table(
    "vacancies_professional_fields",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True),
    Column("professional_field_id", ForeignKey("professional_fields.id"), primary_key=True)
)