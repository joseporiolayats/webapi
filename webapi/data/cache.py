from webapi.data.store_json import JSONDataToCache


class Cache:
    def __init__(self, db_url: str, db_name: str):
        self.db_url = db_url
        self.db_name = db_name
        self.cache = {}

    async def load_data(self) -> dict:
        dataloader = JSONDataToCache(self.db_url)
        await dataloader.load_data_to_cache(name=self.db_name)
        self.cache = await dataloader.get_cache()
        return self.cache
