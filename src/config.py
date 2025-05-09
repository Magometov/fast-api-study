import sys
from typing import Literal

from loguru import logger
from pydantic import BaseModel, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 5432
    name: str = "postgres"
    username: str = "postgres"
    password: SecretStr = SecretStr("postgres")

    def get_url(
        self,
        scheme: Literal["postgres", "postgresql", "postgresql+asyncpg"] = "postgresql+asyncpg",
        db_name: str | None = None,
    ) -> SecretStr:
        dsn = PostgresDsn.build(
            scheme=scheme,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password.get_secret_value(),
            path=db_name or self.name,
        )
        return SecretStr(str(dsn))


class JwtSettings(BaseModel):
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    debug: bool = True
    cors: list[str] = ["http://127.0.0.1"]
    db: DatabaseSettings = DatabaseSettings()
    jwt: JwtSettings = JwtSettings()
    tonapi_url: str = "https://tonapi.io/"


settings = Settings()

# Logging Configuration
logger.remove(0)
logger.add(
    sys.stderr,
    format="<red>[{level}]</red> Message : <green>{message}</green> @ {time:YYYY-MM-DD HH:mm:ss}",
    colorize=True,
    level=("DEBUG" if settings.debug else "INFO"),
    backtrace=True,
    diagnose=True,
)
