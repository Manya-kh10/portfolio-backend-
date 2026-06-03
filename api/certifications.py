from fastapi import APIRouter, HTTPException
from typing import List
from api.database import get_db
from api.models import CertificationSchema

router = APIRouter()

@router.get("/", response_model=List[CertificationSchema])
async def get_certifications():
    """
    Fetches all certifications earned by Manya.
    """
    db = get_db()
    return list(db.certifications.find({}, {'_id': 0}))

@router.post("/", status_code=201)
async def add_new_certification(cert: CertificationSchema):
    """
    Endpoint to easily add a new earned certification.
    """
    db = get_db()
    existing = db.certifications.find_one({"name": cert.name})
    if existing:
        raise HTTPException(status_code=400, detail="Certification with this name already exists.")
        
    db.certifications.insert_one(cert.model_dump())
    return {"message": f"Successfully injected certification: '{cert.name}'!"}