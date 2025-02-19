from fastapi import FastAPI
import httpx
import uvicorn

from subscriber_servise.router import router as sub_router

app = FastAPI(title="SubService",
              version="1.0")

app.include_router(sub_router)

@app.get("/")
async def hello() -> dict:
    return {"message": f'Hello, This is {app.title} version {app.version}'}

@app.get("/hello_to_users")
async def hello_to_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/")
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
