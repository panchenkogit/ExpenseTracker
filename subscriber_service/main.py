from fastapi import FastAPI

import httpx
import uvicorn
from common_utils.redis.client import redis_client

from subscriber_service.router import router as sub_router

app = FastAPI(title="SubService", version="1.0")

app.include_router(sub_router)


@app.get("/")
async def hello() -> dict:
    return {"message": f"Hello, This is {app.title} version {app.version}"}


@app.get("/hello_to_users")
async def hello_to_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/")
        return response.json()


@app.get("/check_redis")
async def check_redis():
    await redis_client.set("test_key", "test_value")
    value = await redis_client.get("test_key")

    if value:
        return {"message": f"Redis is working, test_key: {value}"}
    else:
        return {"message": "Redis is not working"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
