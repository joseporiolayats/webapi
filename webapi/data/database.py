"""
webapi/data/database.py
"""
from typing import Optional

from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from webapi.logs.logger import app_logger

# read the connection string from the environment variables
mongodb_connection_string = config("DB_URL")
db_name = config("DB_NAME")
db_collection_clients = config("DB_COLLECTION_CLIENTS")
db_collection_policies = config("DB_COLLECTION_POLICIES")


class MongoDBAtlasCRUD:
    def __init__(self, client, database: Optional, collection_name: Optional):
        self.connection_string = None
        self.database_name = db_name
        self.collection_name = collection_name or None
        self.client = client
        self.db = None
        self.collection = None
        self.database = database if database is not None else None

    # def __del__(self):
    #     self.client.close()
    #     app_logger.info("Closed the MongoDB Atlas client connection")

    def start_database(
        self,
        connection_string=mongodb_connection_string,
        database_name=db_name,
        collection_name=db_collection_clients,
    ):
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    @classmethod
    async def create_instance(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        await instance._connect()
        return instance

    async def _connect(self):
        try:
            self.client = (
                AsyncIOMotorClient(self.connection_string)
                if self.database is None
                else self.database
            )
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            app_logger.info(
                f"Connected to MongoDB Atlas database {self.database_name} and "
                f"collection {self.collection_name}"
            )
        except PyMongoError as e:
            app_logger.error(f"Error connecting to MongoDB Atlas: {e}")

    async def insert_one(self, document):
        try:
            await self._connect()
            result = await self.collection.insert_one(document)
            app_logger.info(f"Inserted document with ID {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            app_logger.error(f"Error inserting document: {e}")

    async def find_one(self, query):
        try:
            result = await self.collection.find_one(query)
            if result:
                app_logger.info(f"Found document: {result}")
            else:
                app_logger.warning("Document not found")
            return result
        except PyMongoError as e:
            app_logger.error(f"Error finding document: {e}")

    async def update_one(self, query, update):
        try:
            result = await self.collection.update_one(query, update)
            app_logger.info(f"Updated {result.modified_count} document(s)")
            return result.modified_count
        except PyMongoError as e:
            app_logger.error(f"Error updating document: {e}")

    async def delete_one(self, query):
        try:
            result = await self.collection.delete_one(query)
            app_logger.info(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except PyMongoError as e:
            app_logger.error(f"Error deleting document: {e}")
