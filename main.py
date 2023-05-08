"""
main.py

Main script for starting the app
"""
import logging

import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from webapi.data.dataflow import DataFlow
from webapi.routers.clients import router as clients_router
from webapi.routers.policies import router as policies_router
from webapi.routers.users import router as users_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read environment variables
DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)
DB_COLLECTION_CLIENTS = config("DB_COLLECTION_CLIENTS", cast=str)
DB_COLLECTION_POLICIES = config("DB_COLLECTION_POLICIES", cast=str)
DB_CLIENTS = config("DB_CLIENTS", cast=str)
DB_POLICIES = config("DB_POLICIES", cast=str)

# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(policies_router, prefix="/policies", tags=["policies"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(users_router, prefix="/gateway", tags=["gateway"])


@app.on_event("startup")
async def startup_db_client():
    """
    Initialize the database and cache on startup.
    """
    try:
        app.mongodb_client = AsyncIOMotorClient(DB_URL)
        app.mongodb = app.mongodb_client[DB_NAME]
        dataflow = DataFlow(
            client=app.mongodb_client,
            db_names=["clients", "policies"],
            database=app.mongodb,
        )

        collections_in_remote_db = await app.mongodb.list_collection_names()

        if f"{DB_NAME}.{DB_COLLECTION_CLIENTS}" not in collections_in_remote_db:
            await dataflow.fill_database(url=DB_CLIENTS, db_name=DB_COLLECTION_CLIENTS)

        if f"{DB_NAME}.{DB_COLLECTION_POLICIES}" not in collections_in_remote_db:
            await dataflow.fill_database(
                url=DB_POLICIES, db_name=DB_COLLECTION_POLICIES
            )

        app.cache = dataflow.start_cache()
        app.cache["clients"] = await dataflow.load_cache(
            url=DB_CLIENTS, db_name=DB_COLLECTION_CLIENTS
        )
        app.cache["policies"] = await dataflow.load_cache(
            url=DB_POLICIES, db_name=DB_COLLECTION_POLICIES
        )
        logger.info("Database and cache initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database and cache: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    """
    Close the database connection on shutdown.
    """
    try:
        app.mongodb_client.close()
        logger.info("Database connection closed successfully.")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
