from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_database():

    load_dotenv()
    connection_string = os.getenv("MONGODB_CONNECTION_STRING")
    
    if not connection_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable is not set")
    
    client = MongoClient(connection_string)
    db = client['teamdb']
    return db
