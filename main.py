import time
import asyncio
import uuid
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
import boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from debug_toolbar.middleware import DebugToolbarMiddleware
from config import settings
from api.v1.routes import router as api_router_v1


app = FastAPI(
    debug=settings.DEBUG,
    # openapi_url="/api/v1/openapi.json",
    # docs_url="/api/v1/docs",
    # redoc_url="/api/v1/redoc",
    # swagger_ui_oauth2_redirect_url="/api/v1/docs/oauth2-redirect",
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
    print("Sinple api start!!")
    time.sleep(1)
    raise
    return {"message": "Simple fast task!"}


first_executor = ThreadPoolExecutor(max_workers=5)
second_executor = ThreadPoolExecutor(max_workers=25)


def sync_function():
    """Get images from AI server"""
    print("api 서버에 이미지를 요청(최대 5번)")
    # 이미지 파일 경로
    image_path = "test.png"

    # 이미지 열기
    image = Image.open(image_path)

    # 이미지가 RGB 모드인지 확인하고 변환
    if image.mode != "RGB":
        image = image.convert("RGB")

    # 이미지를 NumPy 배열로 변환
    rgb_array = np.array(image)
    
    # 2. NumPy 배열을 이미지로 변환
    image = Image.fromarray(rgb_array)
    
    # 3. 이미지를 바이너리 버퍼에 저장
    buffers = []
    for _ in range(7):
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)  # 버퍼의 시작 위치로 이동
        buffers.append(buffer)
    time.sleep(10)
    return buffers


def second_sync_function(s3_client, bucket_name, buffer):
    """Upload image to S3"""

    # 5. S3에 업로드
    file_name = uuid.uuid4()
    s3_key = f"demo/test/{file_name}.jpeg"
    print(f"s3에 이미지 업로드 최대 25번")
    content_type = "image/jpeg"
    s3_client.upload_fileobj(
        buffer,
        bucket_name,
        s3_key,
        ExtraArgs={
            "ContentType": content_type,
            "CacheControl": "max-age=86400",
            # "ContentDisposition": "inline",  # 브라우저에서 로드
        },
    )
    time.sleep(5)
    return f"Upload complete {s3_key}"


@app.get("/api/v1/slow")
async def slow():
    print("slow api start!!@!@")
    loop = asyncio.get_event_loop()

    # 첫 번째 단계: 최대 5개의 작업을 병렬로 실행
    first_results = await loop.run_in_executor(first_executor, sync_function)

    # 4. S3 클라이언트 생성
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    # 5. S3에 업로드
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # 두 번째 단계: 첫 번째 작업의 결과를 사용하여 최대 7개의 작업을 병렬로 실행
    second_tasks = [
        loop.run_in_executor(
            second_executor, second_sync_function, s3_client, bucket_name, buffer
        )
        for buffer in first_results
    ]
    second_results = await asyncio.gather(*second_tasks)

    return {"first_results": first_results, "second_results": second_results}


app.include_router(api_router_v1)
