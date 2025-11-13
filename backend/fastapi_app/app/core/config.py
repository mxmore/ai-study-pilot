from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    environment: str = Field(default="development")
    postgres_dsn: str = Field(default="postgresql+psycopg://user:pass@localhost:5432/ai_study")
    mongo_dsn: str = Field(default="mongodb://localhost:27017")
    vector_dimension: int = 1536

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()
