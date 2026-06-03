import os
from pymongo import MongoClient
from dotenv import load_dotenv
# Load variables from the hidden .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
# Initialize the MongoDB Client instance
# Serverless functions scale up/down rapidly, so we instantiate the client connection pool globally
client = MongoClient(MONGO_URI)
# Select or create the core database cluster named "portfolio"
db = client.portfolio
def get_db():
    return db
