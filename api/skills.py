from fastapi import APIRouter, HTTPException, Depends
from typing import List
from api.database import get_db, serialize_docs
from api.models import SkillSchema
from bson import ObjectId
from api.auth import verify_admin

router = APIRouter()

@router.get("/", response_model=List[SkillSchema])
async def get_skills():
    """
    Fetches all skills from MongoDB to build the dynamic skill charts in the UI.
    """
    db = get_db()
    skills_cursor = db.skills.find({})
    return serialize_docs(skills_cursor)

@router.post("/", status_code=201)
async def add_new_skill(skill: SkillSchema, authenticated: bool = Depends(verify_admin)):
    """
    Endpoint to easily add a new technical skill.
    """
    db = get_db()
    # Check if this skill already exists
    existing = db.skills.find_one({"name": skill.name})
    if existing:
        raise HTTPException(status_code=400, detail=f"Skill '{skill.name}' already exists.")
    
    skill_dict = skill.model_dump(exclude={"id"})
    db.skills.insert_one(skill_dict)
    return {"message": f"Successfully injected skill: '{skill.name}' into the cluster!"}

@router.put("/{id}")
async def update_skill(id: str, skill: SkillSchema, authenticated: bool = Depends(verify_admin)):
    """
    Update an existing technical skill by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid skill ID format.")
    
    skill_dict = skill.model_dump(exclude={"id"})
    result = db.skills.update_one({"_id": ObjectId(id)}, {"$set": skill_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found.")
    
    return {"message": f"Successfully updated skill '{skill.name}'."}

@router.delete("/{id}")
async def delete_skill(id: str, authenticated: bool = Depends(verify_admin)):
    """
    Delete a technical skill by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid skill ID format.")
    
    result = db.skills.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found.")
    
    return {"message": "Successfully deleted skill."}