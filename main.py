from fastapi import FastAPI
from api.v1.routes import router as api_router_v1

app = FastAPI()

app.include_router(api_router_v1)
