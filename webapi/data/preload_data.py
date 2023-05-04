"""
webapi/data/preload_data.py

This script is used to fill up the database with the given data from the problem
statement.

There will be two calls, one for each data source.

"""
# from decouple import config
import asyncio

from decouple import config

from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.store_json import JSONDataToMongoDB

# read the connection string from the environment variables
mongodb_connection_string = config("DB_URL")
db_name = config("DB_NAME")
db_collection_clients = config("DB_COLLECTION_CLIENTS")
db_collection_policies = config("DB_COLLECTION_POLICIES")

# company clients data source
datasource1 = "https://www.mocky.io/v2/5808862710000087232b75ac"

# company policies data source
datasource2 = "https://www.mocky.io/v2/580891a4100000e8242b75c5"


async def main():
    # Create a MongoDBAtlasCRUD instance
    crud_instance_clients = await MongoDBAtlasCRUD.create_instance(
        collection_name=db_collection_clients
    )
    crud_instance_policies = await MongoDBAtlasCRUD.create_instance(
        collection_name=db_collection_policies
    )

    # Create a JSONDataToMongoDB instance
    json_data_to_mongodb_clients = JSONDataToMongoDB(crud_instance_clients)
    json_data_to_mongodb_policies = JSONDataToMongoDB(crud_instance_policies)

    # Fetch JSON data from a URL
    json_data1 = await json_data_to_mongodb_clients.fetch_data_from_json_url(
        datasource1
    )
    json_data2 = await json_data_to_mongodb_policies.fetch_data_from_json_url(
        datasource2
    )

    # Extract the data from the dictionary
    json_post1 = json_data1["clients"]
    json_post2 = json_data2["policies"]

    # Store JSON data into the MongoDB Atlas database
    await json_data_to_mongodb_clients.store_json_data(json_post1)
    await json_data_to_mongodb_policies.store_json_data(json_post2)


if __name__ == "__main__":
    asyncio.run(main())
