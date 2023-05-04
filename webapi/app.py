"""
webapi/app.py

Just a placeholder starting script.
"""
import uvicorn
from decouple import config
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello FastAPI"}


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
