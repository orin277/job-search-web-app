from pydantic import BaseModel, ConfigDict, Field



class UserRead(BaseModel):
    id: int = Field(gt=0)
    user_type_id: int = Field(gt=0)
    city_id: int | None = Field(default=None, gt=0)
    email: str = Field(min_length=5, max_length=80)
    phone: str = Field(min_length=10, max_length=15)
    hashed_password: str = Field(min_length=8, max_length=60)
    name: str = Field(min_length=1, max_length=30)
    surname: str = Field(min_length=1, max_length=40)

    model_config = ConfigDict(from_attributes=True) 