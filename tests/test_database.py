import asyncio

import pytest
from decouple import config

from webapi.data.database import MongoDBAtlasCRUD

DB_URL = config("DB_URL", cast=str)

database_name = "test_db"
collection_name = "test_collection"


@pytest.fixture(scope="module")
def mongo_crud():
    return asyncio.get_event_loop().run_until_complete(
        MongoDBAtlasCRUD.create_instance(DB_URL, database_name, collection_name)
    )


@pytest.fixture(scope="function")
def insert_document(mongo_crud):
    document = {"key": "value"}
    asyncio.get_event_loop().run_until_complete(mongo_crud.insert_one(document))
    yield document


@pytest.fixture(scope="function")
def remove_document(mongo_crud, insert_document):
    yield
    asyncio.get_event_loop().run_until_complete(mongo_crud.delete_one(insert_document))


def test_find_one(mongo_crud, insert_document):
    query = {"key": "value"}
    result = asyncio.get_event_loop().run_until_complete(mongo_crud.find_one(query))
    assert isinstance(result, dict)


def test_update_one(mongo_crud, insert_document):
    query = {"key": "value"}
    update = {"$set": {"new_key": "new_value"}}
    result = asyncio.get_event_loop().run_until_complete(
        mongo_crud.update_one(query, update)
    )
    assert isinstance(result, int)


def test_delete_one(mongo_crud, insert_document, remove_document):
    query = {"key": "value"}
    result = asyncio.get_event_loop().run_until_complete(mongo_crud.delete_one(query))
    assert isinstance(result, int)
