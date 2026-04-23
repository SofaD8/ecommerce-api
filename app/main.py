from fastapi import FastAPI, Response

from app.core.config import settings
from app.api.api_v1 import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/favicon.ico, include_in_schema=False")
async def favicon():
    return Response(content="", media_type="image/x-icon")


@app.get("/")
async def read_root():
    return {"message": "hello Sofa!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
