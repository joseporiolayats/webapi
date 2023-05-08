"""
webapi/data/dataflow.py

This module establishes the data flow between the source, the cache, and the database.
"""
from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.json_handler import JSONData
from webapi.data.store_json import JSONDataToCache
from webapi.data.store_json import JSONDataToMongoDB
from webapi.logs.logger import app_logger


class DataFlow:
    def __init__(self, db_names, database, client):
        """
        Initialize the DataFlow class.

        Args:
            db_names: A list of database names.
            database: The database instance.
            client: The database client instance.
        """
        self.db_names = db_names
        self.database = database
        self.client = client

    def check_database(self, db_name: str) -> int:
        """
        Count the number of documents in the specified database.

        Args:
            db_name: The name of the database to check.

        Returns:
            The number of documents in the database.
        """
        return self.database[db_name].count_documents({})

    async def load_cache(self, url: str, db_name: str):
        """
        Load data into cache for the specified database.

        Args:
            url: The URL for fetching JSON data.
            db_name: The name of the database to load data into the cache.

        Returns:
            A dictionary of the data in the cache.
        """
        data_handler = JSONDataToCache(url)
        app_logger.info(f"Collection {db_name} filled in cache")
        data = await data_handler.load_data_to_cache(db_name)

        return {d["id"]: d for d in data}

    def start_cache(self):
        """
        Initialize the cache for each database in the list of database names.

        Returns:
            A dictionary containing the initialized cache for each database.
        """
        app_logger.info("Starting cache")
        return {db_name: "" for db_name in self.db_names}

    def dump_cache_into_database(self):
        # Method not implemented
        pass

    def update_cache_from_database(self):
        # Method not implemented
        pass

    async def fill_database(self, url: str, db_name: str):
        """
        Fill the specified database with JSON data fetched from the provided URL.

        Args:
            url: The URL for fetching JSON data.
            db_name: The name of the database to fill.
        """
        json_url = JSONData(url)
        data = await json_url.fetch_data_from_json_url()
        mongodb_crud = MongoDBAtlasCRUD(
            client=self.client, database=self.database, collection_name=db_name
        )
        data_handler = JSONDataToMongoDB(mongodb_crud, url)
        await data_handler.store_json_data(data[db_name])
        app_logger.info(f"Database {db_name} filled.")

    async def load_collection_to_dict(self, db_name: str) -> dict:
        """
        Load a collection from the specified database into a dictionary.

        Args:
            db_name: The name of the database to load the collection from.

        Returns:
            A dictionary containing the data from the collection.
        """
        # Connect to the MongoDB server using motor
        collection = self.database[db_name]

        # Get all documents from the collection as a cursor
        cursor = collection.find({})

        # Convert each document to a Python dictionary and store in a dictionary
        data_dict = {}

        async for document in cursor:
            for field, value in document.items():
                print(f"field: {field}, value: {value}")
                data_dict[field] = value

            app_logger.info(f"Collection {db_name} filled in cache")

        app_logger.info(f"{data_dict} first entry")
        print(data_dict)
        # Return the dictionary
        return data_dict
