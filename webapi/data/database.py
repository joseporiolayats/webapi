import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from webapi.logs.logger import app_logger

# load environment variables from .env file
load_dotenv()

# read the connection string from the environment variables
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")


class MongoDBAtlasCRUD:
    def __init__(
        self,
        connection_string=MONGODB_CONNECTION_STRING,
        database_name="default_db",
        collection_name="default_collection",
    ):
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            app_logger.info(
                f"Connected to MongoDB Atlas database {self.database_name} and "
                f"collection {self.collection_name}"
            )
        except PyMongoError as e:
            app_logger.error(f"Error connecting to MongoDB Atlas: {e}")

    def insert_one(self, document):
        try:
            result = self.collection.insert_one(document)
            app_logger.info(f"Inserted document with ID {result.inserted_id}")
            return result.inserted_id
        except PyMongoError as e:
            app_logger.error(f"Error inserting document: {e}")

    def find_one(self, query):
        try:
            result = self.collection.find_one(query)
            if result:
                app_logger.info(f"Found document: {result}")
            else:
                app_logger.warning("Document not found")
            return result
        except PyMongoError as e:
            app_logger.error(f"Error finding document: {e}")

    def update_one(self, query, update):
        try:
            result = self.collection.update_one(query, update)
            app_logger.info(f"Updated {result.modified_count} document(s)")
            return result.modified_count
        except PyMongoError as e:
            app_logger.error(f"Error updating document: {e}")

    def delete_one(self, query):
        try:
            result = self.collection.delete_one(query)
            app_logger.info(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except PyMongoError as e:
            app_logger.error(f"Error deleting document: {e}")
