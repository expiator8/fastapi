import logging
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from fastapi import Request


ENV_PATH = ".env"


class Settings(BaseSettings):
    """.env 파일 설정 모델"""

    # .env 파일 read
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        # extra="ignore",
        frozen=True,
    )

    # 디버그 모드
    DEBUG: bool = True

    # API 버전
    API_VERSION: str = "v1"

    # JWT Config
    ACCESS_TOKEN_SECRET_KEY: str
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # DB Config
    DB_ENGINE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def database_url(self) -> str:
        return URL.create(
            drivername=self.DB_ENGINE,
            username=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        ).__to_string__(hide_password=not self.DEBUG)

    # Logging Config
    if not DEBUG:
        LOGGING_CONFIG: dict[str, Any] = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "error": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s",
                },
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "%(asctime)s - %(levelname)s - %(message)s",
                },
            },
            "handlers": {
                "error": {
                    "formatter": "error",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/error.log",
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/access.log",
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
            },
            "loggers": {
                "uvicorn.error": {
                    "handlers": ["error"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["access"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
        logging.config.dictConfig(LOGGING_CONFIG)

settings = Settings()
