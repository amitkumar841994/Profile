from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

# uri = os.getenv("mongodb")
uri = "mongodb+srv://amitkumar841994:bAyyuwJouF5lSctK@cluster0.cl04m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client["Profiledb"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("not working properly:>>>>>>>>>>",e)
