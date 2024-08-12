import logging
import time
import asyncio
import datetime
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware
from config import settings
from api.v1.routes import router as api_router_v1




app = FastAPI(
    debug=settings.DEBUG,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    swagger_ui_oauth2_redirect_url="/api/v1/docs/oauth2-redirect",
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 미들웨어 추가
if settings.DEBUG:
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=[
            "debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel",
        ],
    )

@app.get("/api/v1/simple")
def simple():
    time.sleep(1)
    return {"message": "Simple fast task!"}


first_executor = ThreadPoolExecutor(max_workers=5)
second_executor = ThreadPoolExecutor(max_workers=25)


def sync_function():
    """Get images from AI server"""
    time.sleep(10)
    return [1,2,3,4,5,6,7]

def second_sync_function(data):
    """Upload image to S3"""
    time.sleep(5)
    return f"Upload complete {data}"

@app.get("/api/v1/slow")
async def slow():
    loop = asyncio.get_event_loop()

    # 첫 번째 단계: 최대 5개의 작업을 병렬로 실행
    first_results = await loop.run_in_executor(first_executor, sync_function)

    # 두 번째 단계: 첫 번째 작업의 결과를 사용하여 최대 7개의 작업을 병렬로 실행
    second_tasks = [loop.run_in_executor(second_executor, second_sync_function, result) for result in range(7)]
    second_results = await asyncio.gather(*second_tasks)

    return {"first_results": 0, "second_results": second_results}

app.include_router(api_router_v1)
