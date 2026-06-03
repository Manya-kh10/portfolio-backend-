from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from api.database import get_db
from api.models import ContactSchema

router = APIRouter()

@router.post("/", status_code=201)
async def send_message(contact: ContactSchema):
    """
    Ingests and saves a visitor's contact request in MongoDB, auto-recording the timestamp.
    """
    db = get_db()
    contact_data = contact.model_dump()
    contact_data["timestamp"] = datetime.utcnow()
    
    result = db.contacts.insert_one(contact_data)
    if result.inserted_id:
        return {"status": "success", "message": "Message received! Manya will get back to you shortly."}
    raise HTTPException(status_code=500, detail="Failed to save message.")

@router.get("/")
async def get_messages():
    """
    Retrieves all visitor messages (ordered by timestamp) for Manya's personal dashboard.
    """
    db = get_db()
    messages = list(db.contacts.find({}, {"_id": 0}))
    # Convert datetime object to string for clean serialization
    for msg in messages:
        if "timestamp" in msg and isinstance(msg["timestamp"], datetime):
            msg["timestamp"] = msg["timestamp"].isoformat()
    return messages