from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

vacancy_work_location_type = Table(
    "vacancies_work_location_types",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True),
    Column("work_location_type_id", ForeignKey("work_location_types.id"), primary_key=True)
)