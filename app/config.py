# app/config.py
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "JSON Processor API"
    APP_VERSION: str = "0.1.0"

    # MySQL connection details
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "json_user"
    DB_PASSWORD: str = "json_password"
    DB_NAME: str = "json_db"

    class Config:
        env_file = ".env"


settings = Settings()
