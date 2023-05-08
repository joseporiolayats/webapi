from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.json_handler import JSONData
from webapi.data.store_json import JSONDataToCache
from webapi.data.store_json import JSONDataToMongoDB
from webapi.logs.logger import app_logger


class DataFlow:
    def __init__(self, db_names, database, client):
        self.db_names = db_names
        self.database = database
        self.client = client
        self.data_handler = None

    async def check_database(self, db_name: str) -> int:
        try:
            async with MongoDBAtlasCRUD(collection_name=db_name) as crud_instance:
                count = await crud_instance.collection.count_documents({})
            app_logger.info(f"{db_name} has {count} documents")
            return count
        except Exception as e:
            app_logger.error(f"Error checking database {db_name}: {e}")
            raise

    async def load_cache(self, url: str, db_name: str) -> dict:
        try:
            data_handler = JSONDataToCache(url)
            app_logger.info(f"Loading {db_name} into cache")
            data = await data_handler.load_data_to_cache(db_name)
            return {d["id"]: d for d in data}
        except Exception as e:
            app_logger.error(f"Error loading cache for {db_name}: {e}")
            raise

    def start_cache(self):
        app_logger.info("Starting cache")
        return {db_name: "" for db_name in self.db_names}

    def dump_cache_into_database(self):
        # Method not implemented
        pass

    def update_cache_from_database(self):
        # Method not implemented
        pass

    async def fill_database(self, url: str, db_name: str) -> None:
        try:
            json_url = JSONData(url)
            data = await json_url.fetch_data_from_json_url()

            async with MongoDBAtlasCRUD(collection_name=db_name) as mongodb_crud:
                self.data_handler = JSONDataToMongoDB(mongodb_crud, url)
                await self.data_handler.store_json_data(data[db_name])

            app_logger.info(f"Filled database {db_name}")
        except Exception as e:
            app_logger.error(f"Error filling database {db_name}: {e}")
            raise

    async def load_collection_to_dict(self, db_name: str) -> dict:
        try:
            async with MongoDBAtlasCRUD(collection_name=db_name) as crud_instance:
                collection = crud_instance.collection
                cursor = collection.find({})
                data_dict = {}

                async for document in cursor:
                    for field, value in document.items():
                        data_dict[field] = value

                    app_logger.info(f"Loaded {db_name} into dictionary")

            return data_dict
        except Exception as e:
            app_logger.error(f"Error loading collection {db_name} to dict: {e}")
            raise
