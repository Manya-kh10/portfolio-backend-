import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load variables from the hidden .env file
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    logger.warning("MONGO_URI is not set inside the environment variables. Database client is offline.")
    client = None
    db = None
else:
    # Set serverSelectionTimeoutMS to 5000ms (5 seconds) to prevent infinite hangs in serverless env
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.portfolio

def get_db():
    if db is None:
        raise RuntimeError("Database connection is not initialized. Please set MONGO_URI in your environment variables.")
    return db
