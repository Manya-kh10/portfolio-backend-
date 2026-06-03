from fastapi import APIRouter, HTTPException
from typing import List
from api.database import get_db
from api.models import ExperienceSchema

router = APIRouter()

@router.get("/", response_model=List[ExperienceSchema])
async def get_experience():
    """
    Fetches all professional experience records.
    """
    db = get_db()
    return list(db.experience.find({}, {'_id': 0}))

@router.post("/", status_code=201)
async def add_new_experience(exp: ExperienceSchema):
    """
    Endpoint to append new professional experience records.
    """
    db = get_db()
    # Check duplicate company + role
    existing = db.experience.find_one({"company": exp.company, "role": exp.role})
    if existing:
        raise HTTPException(status_code=400, detail="Experience record with this company and role already exists.")
    
    db.experience.insert_one(exp.model_dump())
    return {"message": f"Successfully injected experience: '{exp.role} at {exp.company}'!"}