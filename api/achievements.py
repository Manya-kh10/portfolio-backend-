from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from api.database import get_db, serialize_doc, serialize_docs
from api.models import AchievementSchema
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[AchievementSchema])
async def get_achievements(pinned: Optional[bool] = Query(None)):
    """
    Fetches all achievements. Supports filtering by pinned status.
    """
    db = get_db()
    query = {}
    if pinned is not None:
        query["pinned"] = pinned
    
    achievement_cursor = db.achievements.find(query)
    return serialize_docs(achievement_cursor)

@router.post("/", status_code=201)
async def add_new_achievement(achievement: AchievementSchema):
    """
    Endpoint to append new achievements and hackathon records.
    """
    db = get_db()
    existing = db.achievements.find_one({"title": achievement.title})
    if existing:
        raise HTTPException(status_code=400, detail="Achievement with this title already exists.")
        
    ach_dict = achievement.model_dump(exclude={"id"})
    db.achievements.insert_one(ach_dict)
    return {"message": f"Successfully injected achievement: '{achievement.title}'!"}

@router.put("/{id}")
async def update_achievement(id: str, achievement: AchievementSchema):
    """
    Update an existing achievement record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid achievement ID format.")
    
    ach_dict = achievement.model_dump(exclude={"id"})
    
    result = db.achievements.update_one({"_id": ObjectId(id)}, {"$set": ach_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Achievement not found.")
    
    return {"message": f"Successfully updated achievement '{achievement.title}'."}

@router.delete("/{id}")
async def delete_achievement(id: str):
    """
    Delete an achievement record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid achievement ID format.")
    
    result = db.achievements.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Achievement not found.")
    
    return {"message": "Successfully deleted achievement."}