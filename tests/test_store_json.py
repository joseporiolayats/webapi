import pytest

from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.store_json import JSONDataToMongoDB

test_url = "https://jsonplaceholder.typicode.com/todos"


@pytest.fixture
async def json_data():
    mongo_crud = await MongoDBAtlasCRUD.create_instance()
    return JSONDataToMongoDB(mongo_crud)


@pytest.mark.asyncio
async def test_fetch_data_from_json_url(json_data):
    json_data = await json_data
    data = await json_data.fetch_data_from_json_url(test_url)
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_store_json_data(json_data):
    json_data = await json_data
    data = await json_data.fetch_data_from_json_url(test_url)
    await json_data.store_json_data(data)
    stored_data = await json_data.mongo_crud.find_one({})
    assert stored_data is not None


@pytest.mark.asyncio
async def test_load_data_to_cache(json_data):
    json_data = await json_data
    await json_data.load_data_to_cache(test_url)
    data = await json_data.search_cached_data(test_url, {})
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_search_cached_data(json_data):
    json_data = await json_data
    await json_data.load_data_to_cache(test_url)
    search_params = {"userId": "1"}
    result = await json_data.search_cached_data(test_url, search_params)
    assert isinstance(result, list)
    assert all(item["userId"] == int(search_params["userId"]) for item in result)
