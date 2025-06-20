# backend/app/utils/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId # Import ObjectId for type checking if needed
from typing import Dict, Any

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Basic check to ensure environment variables are loaded
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set.")
if not MONGO_DB_NAME:
    raise ValueError("MONGO_DB_NAME environment variable not set.")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def save_evaluation_result(result_data: dict) -> Dict[str, Any]:
    """
    Saves the complete evaluation result to MongoDB and returns the saved document.
    The input `result_data` should already be prepared from a Pydantic model
    using `model_dump(by_alias=True)`, so it should have '_id' if present,
    or MongoDB will add it upon insertion.
    """
    try:
        evaluations_collection = db.evaluations
        
        # Insert the data. MongoDB will add an _id if not already present.
        insert_result = evaluations_collection.insert_one(result_data)
        
        # Add the inserted _id back to the dictionary.
        # This _id will be a bson.ObjectId type.
        result_data['_id'] = insert_result.inserted_id
        
        # Return the modified dictionary.
        # The Pydantic model in orchestration_service.py will handle
        # its conversion to `PyObjectId` and then to `str` for the API response.
        return result_data
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        # It's better to re-raise the exception so the caller can handle it
        raise