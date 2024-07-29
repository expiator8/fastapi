from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from config import settings


############################################## Mixins ##############################################
class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True, precision=6),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True, precision=6),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )


############################################## JWT ##############################################
TOKEN_URL = f"/api/{settings.API_VERSION}/token"
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=TOKEN_URL,
    description="""로그인을 통해 Access Token 발급 후, API 요청 시 Authorization 헤더를 추가.
> Authorization: Bearer {Access Token}""",
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class JWT:

    JWT_TYPE = "Bearer"

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update(
            {"exp": int(expire.timestamp())},
        )
        encoded_jwt = jwt.encode(
            to_encode,
            settings.ACCESS_TOKEN_SECRET_KEY,
            algorithm=settings.HASH_ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str, secret_key: str) -> dict:
        http_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="",
            headers={"WWW-Authenticate": JWT.JWT_TYPE},
        )
        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[settings.HASH_ALGORITHM],
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            http_exception.detail = f"Token has expired. {e}"
            raise http_exception from e
        except jwt.InvalidTokenError as e:
            http_exception.detail = f"Could not validate credentials. {e}"
            raise http_exception from e
        except Exception as e:
            http_exception.detail = str(e)
            raise http_exception from e
