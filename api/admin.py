import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Response, Depends
from pydantic import BaseModel
from api.auth import verify_admin

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LUX_EDITORIAL_DIR = os.path.join(BASE_DIR, "stitch design", "lux_editorial")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "manya123")

class LoginRequest(BaseModel):
    password: str

@router.post("/login")
async def admin_login(payload: LoginRequest, response: Response):
    """
    Sets a secure HttpOnly session cookie if the password matches the admin credential.
    """
    if payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect admin password.")
    
    response.set_cookie(
        key="admin_session",
        value=ADMIN_PASSWORD,
        httponly=True,
        max_age=86400,  # 1 day
        samesite="lax",
        secure=False    # Set to True in production with HTTPS
    )
    return {"message": "Authenticated successfully!"}

@router.post("/logout")
async def admin_logout(response: Response):
    """
    Clears the admin session cookie to sign out.
    """
    response.delete_cookie(key="admin_session")
    return {"message": "Logged out successfully!"}

@router.get("/session")
async def check_session(authenticated: bool = Depends(verify_admin)):
    """
    Verifies if the current user session is authenticated as admin.
    """
    return {"status": "authenticated"}

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Overwrites the homepage hero avatar image file (manya_avatar.jpg).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image file uploads are permitted.")
    
    avatar_path = os.path.join(LUX_EDITORIAL_DIR, "manya_avatar.jpg")
    try:
        with open(avatar_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"message": "Hero avatar successfully updated!", "url": "/lux_editorial/manya_avatar.jpg"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save avatar image: {str(e)}")

@router.post("/upload-portrait")
async def upload_portrait(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Overwrites the about me portrait image file (manya_portrait.jpg).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image file uploads are permitted.")
    
    portrait_path = os.path.join(LUX_EDITORIAL_DIR, "manya_portrait.jpg")
    try:
        with open(portrait_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"message": "About Me portrait successfully updated!", "url": "/lux_editorial/manya_portrait.jpg"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save portrait image: {str(e)}")
