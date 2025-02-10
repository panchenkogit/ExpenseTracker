from fastapi import FastAPI

from router import router as user_router

import uvicorn

app = FastAPI(title="UserService",
              version="1.0")

app.include_router(user_router)

@app.get("/")
async def hello() -> dict:
    return {"message": f'This is {app.title} version {app.version}'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
