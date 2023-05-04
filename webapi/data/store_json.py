"""
webapi/data/store_json.py
"""
from typing import Dict
from typing import List
from typing import Union

import aiohttp

from webapi.data.database import MongoDBAtlasCRUD
from webapi.logs.logger import app_logger


class JSONDataToMongoDB:
    """A class to fetch JSON data from a URL and store it into a MongoDB
    Atlas database using the MongoDBAtlasCRUD class.

    Attributes:
        mongo_crud (MongoDBAtlasCRUD): An instance of the MongoDBAtlasCRUD
        class.
    """

    def __init__(self, mongo_crud: MongoDBAtlasCRUD):
        """
        Initializes the JSONDataToMongoDB instance with the given
        MongoDBAtlasCRUD instance.

        Args:
            mongo_crud (MongoDBAtlasCRUD): An instance of the
            MongoDBAtlasCRUD class.
        """
        self.mongo_crud = mongo_crud

    async def fetch_data_from_json_url(self, url: str) -> Union[Dict, List, None]:
        """Fetches JSON data from the given URL.

        Args:
            url (str): The URL of the JSON data source.

        Returns:
            Union[Dict, List, None]: The fetched JSON data as a dictionary or a
            list of dictionaries, or None if there's an error.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                app_logger.error(f"Error fetching JSON data from URL: {e}")
                return None

    async def store_json_data(self, data: Union[Dict, List]) -> None:
        """Stores the given JSON data into the MongoDB Atlas database using the
         MongoDBAtlasCRUD instance.

        Args:
            data (Union[Dict, List]): The JSON data as a dictionary or a list
             of dictionaries.

        Returns:
            None
        """
        if data is None:
            app_logger.error("No data to store")
            return

        if isinstance(data, dict):
            await self.mongo_crud.insert_one(data)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    await self.mongo_crud.insert_one(item)
                else:
                    app_logger.error(f"Invalid data format: {item}")
        else:
            app_logger.error(f"Invalid data format: {data}")
