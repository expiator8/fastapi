from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from core.repository.user import UserRepository
from core.entity import user as user_entity
from core import utils
from config import settings
from ..models import user as user_models


class UserService:
    def sign_up(
        db: Session,
        user: user_models.UserCreate,
    ) -> user_entity.User:
        db_user = UserRepository.get_user_by_email(db=db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        return UserRepository.create_user(db=db, user=user)

    def read_user(
        db: Session,
        id: str,
    ) -> user_entity.User:
        db_user = UserRepository.get_user_by_id(db=db, id=id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="회원정보가 없습니다."
            )
        return db_user

    def read_users_me(
        db: Session,
        email: str,
    ) -> user_entity.User:
        user = UserRepository.get_user_by_email(db=db, email=email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원정보가 없습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def login_for_access_token(
        db: Session,
        user: user_entity.User,
    ) -> user_entity.UserAccessToken:
        access_token = utils.JWT.create_access_token(
            data={"sub": user.email},
        )
        token_count = UserRepository.get_user_token_count(db, user)
        if token_count > 2:
            UserRepository.delete_oldest_user_access_token(db, user)
        return UserRepository.create_user_access_token(db, user, access_token)

    def authenticate_user(db, username: str, password: str) -> user_entity.User:
        user = UserRepository.get_user_by_email(db, username)
        if not user or not utils.verify_password(password, user.hashed_password):
            # return False
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Incorrect username or password",
                # headers={"WWW-Authenticate": "Bearer"},
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
