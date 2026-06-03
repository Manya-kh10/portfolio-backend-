from fastapi import APIRouter, HTTPException
from typing import List
from api.database import get_db
from api.models import AchievementSchema

router = APIRouter()

@router.get("/", response_model=List[AchievementSchema])
async def get_achievements():
    """
    Fetches all achievements and awards.
    """
    db = get_db()
    return list(db.achievements.find({}, {'_id': 0}))

@router.post("/", status_code=201)
async def add_new_achievement(achievement: AchievementSchema):
    """
    Endpoint to append new achievements and hackathon records.
    """
    db = get_db()
    existing = db.achievements.find_one({"title": achievement.title})
    if existing:
        raise HTTPException(status_code=400, detail="Achievement with this title already exists.")
        
    db.achievements.insert_one(achievement.model_dump())
    return {"message": f"Successfully injected achievement: '{achievement.title}'!"}