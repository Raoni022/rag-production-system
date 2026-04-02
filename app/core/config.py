from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Production System"
    app_env: str = "development"
    app_debug: bool = True
    default_top_k: int = 3
    min_relevance_score: int = 1

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
