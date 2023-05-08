"""
webapi/data/database.py
"""
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
    """
    A class to handle CRUD operations for MongoDB Atlas.

    Attributes:
        client (AsyncIOMotorClient): An asynchronous MongoDB client.
        db (AsyncIOMotorDatabase): An asynchronous MongoDB database.
        collection (AsyncIOMotorCollection): An asynchronous MongoDB collection.
    """

    def __init__(self, collection_name: str):
        """
        Initializes MongoDBAtlasCRUD with the given collection name.

        Args:
            collection_name (str): The name of the collection to be used.
        """
        self.client = AsyncIOMotorClient(config("DB_URL"))
        self.db = self.client[config("DB_NAME")]
        self.collection = self.db[collection_name]

    @classmethod
    async def create_instance(cls, collection_name: str):
        """
        Creates an instance of MongoDBAtlasCRUD with the given collection name.

        Args:
            collection_name (str): The name of the collection to be used.

        Returns:
            instance (MongoDBAtlasCRUD): An instance of MongoDBAtlasCRUD.
        """
        instance = cls(collection_name)
        await instance._initialize()
        return instance

    async def _initialize(self) -> None:
        """
        Initializes the MongoDBAtlasCRUD instance by checking if the MongoDB server
        is available.

        Returns:
            None
        """
        try:
            await self.client.admin.command("ismaster")
            app_logger.info("Connected to MongoDB server")
        except Exception as e:
            app_logger.error(f"Error initializing MongoDBAtlasCRUD: {e}")
            raise

    async def __aenter__(self):
        """
        Enters the asynchronous context manager.

        Returns:
            self (MongoDBAtlasCRUD): The current instance of MongoDBAtlasCRUD.
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exits the asynchronous context manager and closes the MongoDB connection.

        Args:
            exc_type: The type of exception raised, if any.
            exc_val: The instance of exception raised, if any.
            exc_tb: The traceback object encapsulating the call stack, if any.

        Returns:
            None
        """
        await self.client.close()
        app_logger.info("Closed connection to MongoDB server")

    async def insert_one(self, document: dict) -> str:
        """
        Inserts a single document into the collection.

        Args:
            document (dict): The document to be inserted.

        Returns:
            str: The ObjectId of the inserted document as a string.
        """
        try:
            result = await self.collection.insert_one(document)
            app_logger.info(f"Inserted document with ID: {str(result.inserted_id)}")
            return str(result.inserted_id)
        except Exception as e:
            app_logger.error(f"Error inserting document: {e}")
            raise

    async def find_one(self, query):
        """
        Find a single document in the collection based on a query.

        Args:
            query: The query to filter documents.

        Returns:
            The found document, if any.
        """
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
        """
        Update a single document in the collection based on a query.

        Args:
            query: The query to filter documents.
            update: The update to apply to the document.

        Returns:
            The number of modified documents.
        """
        try:
            result = await self.collection.update_one(query, update)
            app_logger.info(f"Updated {result.modified_count} document(s)")
            return result.modified_count
        except PyMongoError as e:
            app_logger.error(f"Error updating document: {e}")

    async def delete_one(self, query):
        """
        Delete a single document in the collection based on a query.

        Args:
            query: The query to filter documents.

        Returns:
            The number of deleted documents.
        """
        try:
            result = await self.collection.delete_one(query)
            app_logger.info(f"Deleted {result.deleted_count} document(s)")
            return result.deleted_count
        except PyMongoError as e:
            app_logger.error(f"Error deleting document: {e}")
