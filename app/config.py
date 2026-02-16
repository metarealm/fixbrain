# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    data_dir: str = "data"

    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"


settings = Settings()
