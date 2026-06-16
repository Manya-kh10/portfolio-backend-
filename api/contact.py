from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List
from api.database import get_db, serialize_docs
from api.models import ContactSchema
from api.auth import verify_admin

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
async def get_messages(authenticated: bool = Depends(verify_admin)):
    """
    Retrieves all visitor messages (ordered by timestamp descending) for Manya's personal dashboard.
    """
    db = get_db()
    raw_messages = list(db.contacts.find().sort("timestamp", -1))
    messages = serialize_docs(raw_messages)
    # Convert datetime object to string for clean serialization
    for msg in messages:
        if "timestamp" in msg and isinstance(msg["timestamp"], datetime):
            msg["timestamp"] = msg["timestamp"].isoformat()
    return messages

@router.delete("/{message_id}")
async def delete_message(message_id: str, authenticated: bool = Depends(verify_admin)):
    """
    Deletes a specific contact message by its ID.
    """
    db = get_db()
    from bson import ObjectId
    try:
        obj_id = ObjectId(message_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid message ID format.")
    
    result = db.contacts.delete_one({"_id": obj_id})
    if result.deleted_count:
        return {"status": "success", "message": "Message deleted successfully."}
    raise HTTPException(status_code=404, detail="Message not found.")