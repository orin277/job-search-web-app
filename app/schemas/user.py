from pydantic import BaseModel, ConfigDict, Field



class UserRead(BaseModel):
    id: int = Field(gt=0)
    user_role_id: int = Field(gt=0)
    city_id: int | None = Field(default=None, gt=0)
    email: str = Field(min_length=5, max_length=80)
    phone: str = Field(min_length=10, max_length=15)
    name: str = Field(min_length=1, max_length=30)
    surname: str = Field(min_length=1, max_length=40)

    model_config = ConfigDict(from_attributes=True) 


class UserEditBase(BaseModel):
    city_id: int | None = Field(default=None, gt=0)
    email: str | None = Field(default=None, min_length=5, max_length=80)
    phone: str | None = Field(default=None, min_length=10, max_length=15)
    hashed_password: str | None = Field(default=None, min_length=8, max_length=60)
    name: str | None = Field(default=None, min_length=1, max_length=30)
    surname: str | None = Field(default=None, min_length=1, max_length=40)

class UserEdit(UserEditBase):
    id: int = Field(gt=0)