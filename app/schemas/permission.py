from pydantic import BaseModel, ConfigDict, Field


class PermissionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class PermissionEdit(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=120)


class PermissionRead(PermissionEdit):
    model_config = ConfigDict(from_attributes=True)