"""
webapi/data/preload_data.py

This script is used to fill up the database with the given data from the problem
statement.

There will be two calls, one for each data source.

"""
import os

from dotenv import load_dotenv

from webapi.data.database import MongoDBAtlasCRUD
from webapi.data.store_json import JSONDataToMongoDB

# load environment variables from .env file
load_dotenv()

# read the connection string from the environment variables
MONGODB_CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")

# company clients data source
datasource1 = "https://www.mocky.io/v2/5808862710000087232b75ac"

# company policies data source
datasource2 = "https://www.mocky.io/v2/580891a4100000e8242b75c5"

if __name__ == "__main__":
    # Replace this with your MongoDB Atlas connection string.
    connection_string = MONGODB_CONNECTION_STRING

    # Set the database and collection names
    database_name = "customersDB"
    collection_name = "customers"

    # Create a MongoDBAtlasCRUD instance
    mongo_crud = MongoDBAtlasCRUD(connection_string, database_name, collection_name)

    # Create a JSONDataToMongoDB instance
    json_data_to_mongodb = JSONDataToMongoDB(mongo_crud)

    # Fetch JSON data from a URL

    json_data1 = json_data_to_mongodb.fetch_data_from_json_url(datasource1)
    json_data2 = json_data_to_mongodb.fetch_data_from_json_url(datasource2)

    # Store JSON data into the MongoDB Atlas database
    json_data_to_mongodb.store_json_data(json_data1)
    json_data_to_mongodb.store_json_data(json_data2)
