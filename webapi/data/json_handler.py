"""
webapi/data/json_handler.py
"""
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiohttp

from webapi.logs.logger import app_logger


class JSONData:
    def __init__(self, url: str):
        """
        Initialize the JSONData class.

        Args:
            url: The URL for fetching JSON data.
        """
        self.url = url

    async def fetch_data_from_json_url(
        self, url: Optional[str] = None
    ) -> Union[Dict, List, None]:
        """
        Fetch JSON data from the provided URL.

        Args:
            url: The URL for fetching JSON data (optional).

        Returns:
            A dictionary or a list containing the fetched JSON data,
             or None if an error occurs.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                app_logger.error(f"Error fetching JSON data from URL: {e}")
                return None

    async def return_data_in_json(self):
        # Method not implemented
        pass
