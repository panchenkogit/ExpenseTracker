from fastapi import FastAPI
import httpx

from user_service.router import router as user_router

import uvicorn

app = FastAPI(title="UserService",
              version="1.0")

app.include_router(user_router)

@app.get("/")
async def hello() -> dict:
    return {"message": f'Hello, This is {app.title} version {app.version}'}

@app.get("/hello_to_sub")
async def hello_to_sub():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8001/")
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
