from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from api.v1.routes import router as api_router_v1
from config import settings

app = FastAPI(debug=settings.DEBUG)
# 미들웨어 추가
app.add_middleware(
    DebugToolbarMiddleware,
    panels=[
        "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
    ],
)

app.include_router(api_router_v1)
