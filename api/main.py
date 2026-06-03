from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.projects import router as projects_router
from api.contact import router as contact_router
from api.certifications import router as certs_router
from api.experience import router as experience_router
from api.achievements import router as achievements_router
from api.skills import router as skills_router
from api.chat import router as chat_router

app = FastAPI(
    title="Manya Khandelwal Portfolio Backend",
    description="Serverless FastAPI gateway driving project portfolios, visitor contact requests, and Digital Twin AI interactions.",
    version="1.0.0"
)

# Configure CORS to permit interactions from frontend development and hosting frameworks
origins = ["http://localhost:3000", "http://localhost:5173", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all gateway routers with standard prefixes and tags
app.include_router(skills_router, prefix="/api/skills", tags=["Skills Collection"])
app.include_router(achievements_router, prefix="/api/achievements", tags=["Achievements Collection"])
app.include_router(experience_router, prefix="/api/experience", tags=["Experience Collection"])
app.include_router(certs_router, prefix="/api/certifications", tags=["Certifications Collection"])
app.include_router(projects_router, prefix="/api/projects", tags=["Projects Collection"])
app.include_router(contact_router, prefix="/api/contact", tags=["Contact Submissions"])
app.include_router(chat_router, prefix="/api/chat", tags=["Digital Twin Conversational Intelligence"])

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Mount the static assets folder to serve background artwork and styling files
app.mount("/lux_editorial", StaticFiles(directory="stitch design/lux_editorial"), name="lux_editorial")

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """
    Serves Manya's main Lux Editorial portfolio home page.
    """
    path = os.path.join("stitch design", "home", "code.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/projects", response_class=HTMLResponse)
async def serve_projects_layout_1():
    """
    Serves the standard editorial card grid layout for Projects.
    """
    path = os.path.join("stitch design", "project", "code.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/experience", response_class=HTMLResponse)
async def serve_experience():
    """
    Serves the professional journey experience page.
    """
    path = os.path.join("stitch design", "experience", "code.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/certifications", response_class=HTMLResponse)
async def serve_certifications():
    """
    Serves the accredited skills and credentials page.
    """
    path = os.path.join("stitch design", "certifcations", "code.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/achievements", response_class=HTMLResponse)
async def serve_achievements():
    """
    Serves the milestones and key accolades page.
    """
    path = os.path.join("stitch design", "achievements", "code.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/status")
async def root():
    return {
        "status": "online",
        "message": "Welcome to Manya's Digital Twin Portfolio API Gateway.",
        "deployment_platform": "Vercel Serverless"
    }