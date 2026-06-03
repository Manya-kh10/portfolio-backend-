from fastapi import APIRouter, HTTPException
from api.database import get_db
from api.models import ProjectSchema
from typing import List
router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
async def get_all_projects():
    """
    Fetches all projects from MongoDB to drive your category selection UI.
    """
    db = get_db()
    # Grab all records from our database's "projects" collection
    projects_cursor = db.projects.find({}, {"_id": 0})
    return list(projects_cursor)

@router.post("/", status_code=201)
async def add_new_project(project: ProjectSchema):
    """
    Endpoint to easily add a new project to your portfolio database via JSON.
    """
    db = get_db()
    # Check if a project with the same title already exists to prevent duplicate entries
    existing = db.projects.find_one({"title": project.title})
    if existing:
        raise HTTPException(status_code=400, detail="A project with this title already exists.")
    # Convert Pydantic object to native Python dictionary data type for MongoDB ingestion
    db.projects.insert_one(project.model_dump())
    return {"message": f"Successfully injected project: '{project.title}' into the cluster!"}
