# app/config.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    data_dir: str = os.getenv("FIXBRAIN_DATA_DIR", "data")

    class Config:
        env_file = ".env"


settings = Settings()
