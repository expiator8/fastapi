from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL
from fastapi import Request
import sqltap

ENV_PATH = ".env"


class Settings(BaseSettings):
    """.env 파일 설정 모델"""

    # .env 파일 read
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        # extra="ignore",
        # frozen=True,
    )

    API_VERSION: str = "v1"

    # JWT
    ACCESS_TOKEN_SECRET_KEY: str
    HASH_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 디버그 모드
    DEBUG: bool = True

    # 데이터베이스 설정
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
        ).__to_string__(hide_password=False)

    # # Middleware
    # async def sqltap_profiler(self, request: Request, call_next):
    #     profiler = sqltap.start()
    #     response = await call_next(request)
    #     stats = profiler.collect()
    #     request.state.profiler_stats = stats
    #     return response


settings = Settings()
