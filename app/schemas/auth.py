from datetime import date, datetime, timezone
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenCreate(BaseModel):
    user_id: int = Field(gt=0)
    token: str = Field(min_length=1, max_length=64)
    revoked: bool = Field(default=False)
    user_agent: str | None = Field(min_length=1, max_length=512)
    ip_address: str | None = Field(min_length=15, max_length=45)
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    expires_at: datetime = Field()