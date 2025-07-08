from sqlalchemy import Table, Column, ForeignKey, Integer
from app.db.database import Base

vacancy_city = Table(
    "vacancies_cities",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancies.id"), primary_key=True),
    Column("city_id", ForeignKey("cities.id"), primary_key=True)
)