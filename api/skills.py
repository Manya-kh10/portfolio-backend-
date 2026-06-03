from fastapi import APIRouter, HTTPException
from typing import List
from api.database import get_db
from api.models import SkillSchema

router = APIRouter()

@router.get("/", response_model=List[SkillSchema])
async def get_skills():
    """
    Fetches all skills from MongoDB to build the dynamic skill charts in the UI.
    """
    db = get_db()
    return list(db.skills.find({}, {'_id': 0}))

@router.post("/", status_code=201)
async def add_new_skill(skill: SkillSchema):
    """
    Endpoint to easily add a new technical skill.
    """
    db = get_db()
    # Check if this skill already exists
    existing = db.skills.find_one({"name": skill.name})
    if existing:
        raise HTTPException(status_code=400, detail=f"Skill '{skill.name}' already exists.")
    
    db.skills.insert_one(skill.model_dump())
    return {"message": f"Successfully injected skill: '{skill.name}' into the cluster!"}