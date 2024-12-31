# from pymongo.mongo_client import MongoClient

# # MongoDB connection URI
# uri = "mongodb://amitkumar841994:bAyyuwJouF5lSctK@cluster0.cl04m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create MongoDB client
# client = MongoClient(uri)

# # Connect to the database
# try:
#     client.admin.command("ping")
#     print("Pinged your deployment. Successfully connected to MongoDB!")
# except Exception as e:
#     print("Error connecting to MongoDB:", e)

# # Define a database instance
# db = client["profile"]  # Replace "mydatabase" with your database name



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://amitkumar841994:bAyyuwJouF5lSctK@cluster0.cl04m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["Profiledb"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)