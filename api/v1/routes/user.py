from typing_extensions import Annotated
from fastapi import APIRouter, status, Path, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.database import db_session
from core import utils
from ..models import user as user_models
from ..service.user import UserService

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


@router.get(
    "/users/me",
    summary="프로필 정보 조회",
    status_code=status.HTTP_200_OK,
    response_model=user_models.User,
)
def read_users_me(
    db: db_session,
    token: Annotated[str, Depends(utils.oauth2_scheme)],
):
    email = UserService.authenticate_access_token(db, token)
    return UserService.read_users_me(db=db, email=email)


@router.get(
    "/users/{mb_id}",
    summary="회원 정보 조회",
    status_code=status.HTTP_200_OK,
    response_model=user_models.User,
)
def read_user(
    db: db_session,
    mb_id: Annotated[str, Path(title="회원 아이디", description="회원 아이디")],
):
    return UserService.read_user(db=db, id=mb_id)


@router.post("/token", response_model=user_models.Token)
def login_for_access_token(
    db: db_session,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    return UserService.login_for_access_token(db, user)
