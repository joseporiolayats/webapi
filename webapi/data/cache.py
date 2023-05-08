from webapi.data.store_json import JSONDataToCache


class Cache:
    """
    Cache class for loading and storing data.
    """

    def __init__(self, db_url: str, db_name: str):
        """
        Initialize the Cache object.

        Args:
            db_url (str): Database URL.
            db_name (str): Database name.
        """
        self.db_url = db_url
        self.db_name = db_name
        self.cache = {}

    async def load_data(self) -> dict:
        """
        Load data into the cache using JSONDataToCache.

        Returns:
            dict: The cache containing the loaded data.
        """
        dataloader = JSONDataToCache(self.db_url)
        await dataloader.load_data_to_cache(name=self.db_name)
        self.cache = await dataloader.get_cache()
        return self.cache
