from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiohttp

from webapi.logs.logger import app_logger


class JSONData:
    def __init__(self, url: str):
        self.url = url

    async def fetch_data_from_json_url(
        self, url: Optional[str] = None
    ) -> Union[Dict, List, None]:
        # if self.url is None and url is None:
        #     app_logger.error("No url provided")
        #     raise ValueError("Can't fetch data")

        # self.url = url if url is not None else next

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.url) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                app_logger.error(f"Error fetching JSON data from URL: {e}")
                return None

    async def return_data_in_json(self):
        pass
