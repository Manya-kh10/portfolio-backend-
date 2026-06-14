import os
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LUX_EDITORIAL_DIR = os.path.join(BASE_DIR, "stitch design", "lux_editorial")

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...)):
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
async def upload_portrait(file: UploadFile = File(...)):
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
