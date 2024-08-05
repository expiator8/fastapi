from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI
from api.v1.routes import router as api_router_v1
from config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(debug=settings.DEBUG)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 추가
app.add_middleware(
    DebugToolbarMiddleware,
    panels=[
        "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
    ],
)

app.include_router(api_router_v1)
