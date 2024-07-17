from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.repository.user import UserRepository
from core.entity import user as user_entity
from ..models import user as user_models


class UserService:
    def sign_up(
        db: Session,
        user: user_models.UserCreate,
    ) -> user_entity.User:
        db_user = UserRepository.get_user_by_email(db=db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return UserRepository.create_user(db=db, user=user)
