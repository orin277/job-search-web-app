from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserRead


class ApplicantFilter(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=30)
    surname: str | None = Field(default=None, min_length=1, max_length=40)
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)


class ApplicantRead(BaseModel):
    id: int = Field(gt=0)
    user: UserRead

    model_config = ConfigDict(from_attributes=True) 


class ApplicantCreate(BaseModel):
    city_id: int | None = Field(default=None, gt=0)
    email: str = Field(min_length=5, max_length=80)
    phone: str = Field(min_length=10, max_length=15)
    hashed_password: str = Field(min_length=8, max_length=60)
    name: str = Field(min_length=1, max_length=30)
    surname: str = Field(min_length=1, max_length=40)


class ApplicantEdit(BaseModel):
    id: int = Field(gt=0)
    city_id: int | None = Field(default=None, gt=0)
    email: str | None = Field(default=None, min_length=5, max_length=80)
    phone: str | None = Field(default=None, min_length=10, max_length=15)
    hashed_password: str | None = Field(default=None, min_length=8, max_length=60)
    name: str | None = Field(default=None, min_length=1, max_length=30)
    surname: str | None = Field(default=None, min_length=1, max_length=40)