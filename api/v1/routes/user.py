from fastapi import APIRouter, status
from core.database import db_session
from ..service.user import UserService
from ..models import user as user_models

router = APIRouter()


@router.post(
    "/users",
    summary="회원 가입",
    status_code=status.HTTP_201_CREATED,
    response_model=user_models.User,
)
def sign_up(
    db: db_session,
    user: user_models.UserCreate,
):
    return UserService.sign_up(db=db, user=user)
