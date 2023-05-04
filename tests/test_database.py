"""
webapi/tests/test_database.py
"""
import os

import pytest

from webapi.data.database import MongoDBAtlasCRUD


# Replace this with your MongoDB Atlas connection string.
connection_string = os.getenv("MONGODB_CONNECTION_STRING")

# Set the database and collection names
database_name = "test_db"
collection_name = "test_collection"


@pytest.fixture(scope="module")
def mongo_crud():
    return MongoDBAtlasCRUD(connection_string, database_name, collection_name)


def test_insert_one(mongo_crud):
    document = {"name": "Jane Doe", "age": 28, "city": "San Francisco"}
    inserted_id = mongo_crud.insert_one(document)
    assert inserted_id is not None


def test_find_one(mongo_crud):
    query = {"name": "Jane Doe"}
    result = mongo_crud.find_one(query)
    assert result is not None
    assert result["name"] == "Jane Doe"
    assert result["age"] == 28
    assert result["city"] == "San Francisco"


def test_update_one(mongo_crud):
    query = {"name": "Jane Doe"}
    update = {"$set": {"age": 29}}
    modified_count = mongo_crud.update_one(query, update)
    assert modified_count == 1
    updated_result = mongo_crud.find_one(query)
    assert updated_result["age"] == 29


def test_delete_one(mongo_crud):
    query = {"name": "Jane Doe"}
    deleted_count = mongo_crud.delete_one(query)
    assert deleted_count == 1
    result_after_deletion = mongo_crud.find_one(query)
    assert result_after_deletion is None
