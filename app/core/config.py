from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8'
    )

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db.user}:{self.db.password}@{self.db.host}:{self.db.port}/{self.db.name}"
    
    @property
    def auth_data(self):
        return {"secret_key": self.auth.secret_key, 
            "algorithm": self.auth.algorithm, 
            "access_token_expire_minutes": self.auth.access_token_expire_minutes
        }




settings = Settings()

print(settings.model_dump())