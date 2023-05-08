from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.json_handler import JSONData
from webapi.logs.logger import app_logger


class JSONDataToMongoDB(JSONData):
    def __init__(self, mongo_crud: MongoDBAtlasCRUD, url: Optional[str]):
        super().__init__(url)
        self.mongo_crud = mongo_crud

    async def store_json_data(self, data: Union[Dict, List], database=None) -> None:
        if data is None:
            app_logger.error("No data to store")
            return
        # if database is None:
        #     database = self.mongo_crud

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


class JSONDataToCache(JSONData):
    def __init__(self, url: str = None):
        super().__init__(url)
        self.url = url
        self.cache = {}

    async def load_data_to_cache(self, name: str) -> dict[Any, Any]:
        """
        Load the data from URL in a dictionary to act as cache.
        Args:
            name: Name of the cached data

        Returns:
            None
        """
        data = await self.fetch_data_from_json_url(self.url)
        self.cache[name] = data[name]

        return data[name]

    async def search_cached_data(
        self, name: str, search_params: Dict[str, str]
    ) -> Union[List, None]:
        if self.cache.get(name):
            return [
                await self._search_dict(data, search_params)
                for data in self.cache[name]
                if await self._search_dict(data, search_params)
            ]
        app_logger.error(
            f"Error searching cached data: URL not found in cache: {self.url}"
        )
        return None

    @staticmethod
    async def _search_dict(
        data: Dict, search_params: Dict[str, str]
    ) -> Union[Dict, None]:
        return next(
            (
                None
                for key, value in search_params.items()
                if key not in data or str(data[key]) != value
            ),
            data,
        )

    async def get_cache(self):
        return self.cache
