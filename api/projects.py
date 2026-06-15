from fastapi import APIRouter, HTTPException, Query, Depends
from api.database import get_db, serialize_doc, serialize_docs
from api.models import ProjectSchema
from typing import List, Optional
from bson import ObjectId
from api.auth import verify_admin

router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
async def get_all_projects(pinned: Optional[bool] = Query(None)):
    """
    Fetches projects from MongoDB. Supports filtering by pinned status.
    """
    db = get_db()
    query = {}
    if pinned is not None:
        query["pinned"] = pinned
    
    projects_cursor = db.projects.find(query)
    return serialize_docs(projects_cursor)

@router.post("/", status_code=201)
async def add_new_project(project: ProjectSchema, authenticated: bool = Depends(verify_admin)):
    """
    Endpoint to easily add a new project to your portfolio database via JSON.
    """
    db = get_db()
    existing = db.projects.find_one({"title": project.title})
    if existing:
        raise HTTPException(status_code=400, detail="A project with this title already exists.")
    
    # Exclude id when storing in MongoDB (MongoDB creates _id automatically)
    project_dict = project.model_dump(exclude={"id"})
    db.projects.insert_one(project_dict)
    return {"message": f"Successfully injected project: '{project.title}' into the cluster!"}

@router.put("/{id}")
async def update_project(id: str, project: ProjectSchema, authenticated: bool = Depends(verify_admin)):
    """
    Update an existing project by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid project ID format.")
    
    # Exclude id when updating in MongoDB
    project_dict = project.model_dump(exclude={"id"})
    
    result = db.projects.update_one({"_id": ObjectId(id)}, {"$set": project_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found.")
    
    return {"message": f"Successfully updated project '{project.title}'."}

@router.delete("/{id}")
async def delete_project(id: str, authenticated: bool = Depends(verify_admin)):
    """
    Delete a project by MongoDB ID.
    """
    db = get_db()
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid project ID format.")
    
    result = db.projects.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found.")
    
    return {"message": "Successfully deleted project."}
