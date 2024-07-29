from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, func, delete
from api.v1.models import user as user_models
from config import settings
from ..entity import user as user_entity
from .. import utils


class UserRepository:
    def authenticate_user(db, username: str, password: str) -> user_entity.User:
        user = UserRepository.get_user_by_email(db, username)
        if not user or not utils.verify_password(password, user.hashed_password):
            # return False
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect username or password",
            )
        return user

    def authenticate_access_token(db: Session, access_token: str):
        payload = utils.JWT.decode_token(
            access_token,
            settings.ACCESS_TOKEN_SECRET_KEY,
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_entry = UserRepository.get_user_access_token(db, access_token)
        if not token_entry:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not found in the database",
            )
        return email

    def get_user_by_email(
        db: Session,
        email: str,
    ) -> user_entity.User | None:
        return db.scalar(
            select(user_entity.User).where(user_entity.User.email == email)
        )

    def get_user_by_id(
        db: Session,
        id: str,
    ) -> user_entity.User | None:
        return db.scalar(select(user_entity.User).where(user_entity.User.id == id))

    def create_user(
        db: Session,
        user: user_models.UserCreate,
    ) -> user_entity.User:
        # hashed_password = utils.get_password_hash(user.password)
        hashed_password = utils.pwd_context.hash(user.password)
        db_user = db.scalar(
            insert(user_entity.User)
            .values(
                username=user.username,
                email=user.email,
                hashed_password=hashed_password,
            )
            .returning(user_entity.User)
        )
        db.commit()
        return db_user

    def get_user_token_count(
        db: Session,
        user: user_entity.User,
    ):
        # 특정 user.id에 대한 Access Token row 개수
        return db.scalar(
            select(func.count(user_entity.UserAccessToken.id)).where(
                user_entity.UserAccessToken.user_id == user.id
            )
        )

    def delete_oldest_user_access_token(
        db: Session,
        user: user_entity.User,
    ):
        # 가장 오래전 생성된 Access Token 삭제
        subquery = (
            select(user_entity.UserAccessToken.id)
            .where(user_entity.UserAccessToken.user_id == user.id)
            .order_by(user_entity.UserAccessToken.created_at.asc())
            .limit(1)
        )
        db.execute(
            delete(user_entity.UserAccessToken).where(
                user_entity.UserAccessToken.id == subquery.scalar_subquery()
            )
        )

    def create_user_access_token(
        db: Session,
        user: user_entity.User,
        access_token: str,
    ) -> user_entity.UserAccessToken:
        # Access Token 생성
        db_user_access_token = db.scalar(
            insert(user_entity.UserAccessToken)
            .values(
                user_id=user.id,
                access_token=access_token,
            )
            .returning(user_entity.UserAccessToken)
        )
        db.commit()
        return db_user_access_token

    def get_user_access_token(db: Session, access_token: str):
        return db.scalar(
            select(user_entity.UserAccessToken).where(
                user_entity.UserAccessToken.access_token == access_token
            )
        )
