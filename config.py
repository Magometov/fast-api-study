from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    cors: list[str] = ['http://127.0.0.1']


settings = Settings()