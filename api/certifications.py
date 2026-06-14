from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from api.database import get_db, serialize_doc, serialize_docs
from api.models import CertificationSchema
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[CertificationSchema])
async def get_certifications(pinned: Optional[bool] = Query(None)):
    """
    Fetches all certifications. Supports filtering by pinned status.
    """
    db = get_db()
    query = {}
    if pinned is not None:
        query["pinned"] = pinned
    
    cert_cursor = db.certifications.find(query)
    return serialize_docs(cert_cursor)

@router.post("/", status_code=201)
async def add_new_certification(cert: CertificationSchema):
    """
    Endpoint to easily add a new earned certification.
    """
    db = get_db()
    existing = db.certifications.find_one({"name": cert.name})
    if existing:
        raise HTTPException(status_code=400, detail="Certification with this name already exists.")
        
    cert_dict = cert.model_dump(exclude={"id"})
    db.certifications.insert_one(cert_dict)
    return {"message": f"Successfully injected certification: '{cert.name}'!"}

@router.put("/{id}")
async def update_certification(id: str, cert: CertificationSchema):
    """
    Update an existing certification record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid certification ID format.")
    
    cert_dict = cert.model_dump(exclude={"id"})
    
    result = db.certifications.update_one({"_id": ObjectId(id)}, {"$set": cert_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Certification not found.")
    
    return {"message": f"Successfully updated certification '{cert.name}'."}

@router.delete("/{id}")
async def delete_certification(id: str):
    """
    Delete a certification record by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid certification ID format.")
    
    result = db.certifications.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Certification not found.")
    
    return {"message": "Successfully deleted certification."}