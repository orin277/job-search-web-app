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

class RedisSettings(BaseSettings):
    HOST: str
    PORT: int
    DB: int
    PASSWORD: str

    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    model_config = SettingsConfigDict(
        env_prefix="AUTH_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

class Settings(BaseSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
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
    def redis_db_url(self):
        return f"redis://:{self.redis.PASSWORD}@{self.redis.HOST}:{self.redis.PORT}/{self.redis.DB}"
    
    @property
    def auth_data(self):
        return {"secret_key": self.auth.SECRET_KEY, 
            "algorithm": self.auth.ALGORITHM, 
            "access_token_expire_minutes": self.auth.ACCESS_TOKEN_EXPIRE_MINUTES
        }




settings = Settings()

print(settings.model_dump())