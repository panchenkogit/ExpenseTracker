from fastapi import FastAPI

import uvicorn

app = FastAPI(title="ExpenseTracker", version="1.0")


@app.get("/")
async def hello() -> dict:
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
