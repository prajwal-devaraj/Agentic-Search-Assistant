from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("../../.env", ".env"), extra="ignore")

    prajna_env: str = "development"
    prajna_api_host: str = "0.0.0.0"
    prajna_api_port: int = 8000
    prajna_cors_origins: str = "http://localhost:3000,http://localhost:8081"

    prajna_model_provider: str = "demo"
    prajna_search_provider: str = "demo"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6"
    brave_search_api_key: str | None = None

    database_url: str | None = None
    redis_url: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [x.strip() for x in self.prajna_cors_origins.split(",") if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
