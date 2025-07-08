from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

vacancy_employment_type = Table(
    "vacancies_employment_types",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True),
    Column("employment_type_id", ForeignKey("employment_types.id"), primary_key=True)
)