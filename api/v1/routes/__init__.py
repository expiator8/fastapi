from fastapi import APIRouter
from api.v1.routes import user

router = APIRouter(prefix="/api/v1")

router.include_router(user.router, tags=["회원"])
