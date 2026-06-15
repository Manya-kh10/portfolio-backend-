from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from api.database import get_db, serialize_doc, serialize_docs
from api.models import ExperienceSchema
from bson import ObjectId
from api.auth import verify_admin

router = APIRouter()

@router.get("/", response_model=List[ExperienceSchema])
async def get_experience(pinned: Optional[bool] = Query(None)):
    """
    Fetches experience records. Supports filtering by pinned status.
    """
    db = get_db()
    query = {}
    if pinned is not None:
        query["pinned"] = pinned
    
    experience_cursor = db.experience.find(query)
    return serialize_docs(experience_cursor)

@router.post("/", status_code=201)
async def add_new_experience(exp: ExperienceSchema, authenticated: bool = Depends(verify_admin)):
    """
    Endpoint to append new professional experience records.
    """
    db = get_db()
    existing = db.experience.find_one({"company": exp.company, "role": exp.role})
    if existing:
        raise HTTPException(status_code=400, detail="Experience record with this company and role already exists.")
    
    exp_dict = exp.model_dump(exclude={"id"})
    db.experience.insert_one(exp_dict)
    return {"message": f"Successfully injected experience: '{exp.role} at {exp.company}'!"}

@router.put("/{id}")
async def update_experience(id: str, exp: ExperienceSchema, authenticated: bool = Depends(verify_admin)):
    """
    Update an existing experience record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid experience ID format.")
    
    exp_dict = exp.model_dump(exclude={"id"})
    
    result = db.experience.update_one({"_id": ObjectId(id)}, {"$set": exp_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Experience record not found.")
    
    return {"message": f"Successfully updated experience: '{exp.role} at {exp.company}'."}

@router.delete("/{id}")
async def delete_experience(id: str, authenticated: bool = Depends(verify_admin)):
    """
    Delete an experience record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid experience ID format.")
    
    result = db.experience.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Experience record not found.")
    
    return {"message": "Successfully deleted experience record."}