import os
import uuid
import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Response, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from api.auth import verify_admin
from api.database import get_db
from api.models import ChatbotSettingsSchema
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LUX_EDITORIAL_DIR = os.path.join(BASE_DIR, "stitch design", "lux_editorial")

def get_admin_password():
    return os.getenv("ADMIN_PASSWORD", "manya123")

def get_google_config():
    return {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/admin/google-callback"),
        "admin_email": os.getenv("ADMIN_EMAIL", "khandelwalmanya8@gmail.com")
    }

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def admin_login(payload: LoginRequest, response: Response):
    """
    Sets a secure HttpOnly session cookie if both email and password match the admin credentials.
    """
    config = get_google_config()
    admin_email = config["admin_email"]
    admin_password = get_admin_password()
    
    if payload.email.lower() != admin_email.lower() or payload.password != admin_password:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    response.set_cookie(
        key="admin_session",
        value=admin_password,
        httponly=True,
        max_age=86400,  # 1 day
        samesite="lax",
        secure=False    # Set to True in production with HTTPS
    )
    return {"message": "Authenticated successfully!"}

@router.get("/login/google")
async def google_login():
    """
    Initiates Google OAuth2 sign-in flow by redirecting browser to Google Consent screen.
    """
    config = get_google_config()
    client_id = config["client_id"]
    redirect_uri = config["redirect_uri"]
    if not client_id:
        raise HTTPException(
            status_code=400, 
            detail="Google OAuth is not configured on the server. Please set GOOGLE_CLIENT_ID in your .env file."
        )
    
    scope = "https://www.googleapis.com/auth/userinfo.email openid"
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state=google"
    )
    return RedirectResponse(auth_url)

@router.get("/google-callback")
async def google_callback(code: str, response: Response):
    """
    Receives callback code from Google, exchanges it for access token, fetches profile info,
    and logs the admin in if the email matches.
    """
    config = get_google_config()
    client_id = config["client_id"]
    client_secret = config["client_secret"]
    redirect_uri = config["redirect_uri"]
    admin_email = config["admin_email"]
    admin_password = get_admin_password()
    
    if not client_id or not client_secret:
        raise HTTPException(status_code=400, detail="Google OAuth is not configured on the server.")
    
    async with httpx.AsyncClient() as client:
        try:
            token_res = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            )
            token_data = token_res.json()
            if token_res.status_code != 200:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Token exchange failed: {token_data.get('error_description', 'Unknown error')}"
                )
            
            access_token = token_data.get("access_token")
            
            userinfo_res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo = userinfo_res.json()
            if userinfo_res.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to retrieve profile information.")
            
            email = userinfo.get("email")
            if not email:
                raise HTTPException(status_code=400, detail="Could not retrieve email address from profile.")
            
            if email.lower() != admin_email.lower():
                return RedirectResponse(url="/admin?error=unauthorized_email")
            
            response_redirect = RedirectResponse(url="/admin")
            response_redirect.set_cookie(
                key="admin_session",
                value=admin_password,
                httponly=True,
                max_age=86400,
                samesite="lax",
                secure=False
            )
            return response_redirect
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Google Authentication failed: {str(e)}")


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

@router.get("/chatbot-settings")
async def get_chatbot_settings():
    """
    Fetches current bio context and rules from chatbot_settings collection.
    """
    db = get_db()
    settings = db.chatbot_settings.find_one()
    if not settings:
        return {
            "bio": "Manya is an engineering student working majorly in the domain of AI/ML. She builds AI systems — RAG pipelines, multi-agent platforms, automation workflows. She's skilled in Python, LangChain, and n8n.",
            "custom_instructions": "1. SHORT ANSWERS ONLY. Maximum 2-3 lines. Never write essays or long paragraphs. Be extremely concise.\n2. Always fetch from your tool before answering questions about projects, skills, certifications, or achievements. Never guess or hallucinate.\n3. If someone asks what Manya has built, list project names with one-line descriptions and tell them to check the Projects section for details.\n4. Redirect naturally — if someone wants to know more, point them: \"You can explore the Projects section\", \"Check out her Skills section\", etc.\n5. Be friendly and human. No corporate buzzwords. Just clear, warm, direct replies.\n6. If a section is empty, say: \"Manya's updating that section — check back soon!\"\n7. Never mention tools, databases, APIs, JSON, or any technical internals.\n8. For contact/hiring, say: \"You can reach out to Manya directly via email by clicking the button below.\" and provide the Email button link.\n9. For Resume, LinkedIn, GitHub, or Email: DO NOT provide raw text links. Instead, use markdown link syntax [Button Text](URL) so the frontend can render them as buttons. Use the following URLs:\n   - Resume: [Access Resume](https://github.com/Manya-kh10/Manya-resume/blob/main/Manya_Khandelwal_resume%20%282%29.pdf)\n   - GitHub: [GitHub Profile](https://github.com/Manya-kh10)\n   - LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/manya-khandelwal-b821492a3)\n   - Email: [Send Email](mailto:khandelwalmanya8@gmail.com)\n   Always introduce the button with a professional sentence, e.g., \"Please click on the button below to access Manya's resume.\" or \"You can explore her projects on GitHub via the button below.\"\n10. If asked about AI projects or AI skills, suggest ONLY the properly AI-centered projects: \"NEXUS — Multi-Agent Data Analysis Platform\" and \"Personal RAG Chatbot\". Do not suggest other projects.\n11. If asked about professional experience, always reply with: \"Manya has no industry experience yet, but she is currently gaining practical experience by building real world projects.\" Do not list any other experience."
        }
    return {
        "bio": settings.get("bio", ""),
        "custom_instructions": settings.get("custom_instructions", "")
    }

@router.put("/chatbot-settings")
async def save_chatbot_settings(payload: ChatbotSettingsSchema, authenticated: bool = Depends(verify_admin)):
    """
    Saves updated biography context and custom instructions.
    """
    db = get_db()
    db.chatbot_settings.update_one(
        {}, 
        {"$set": payload.model_dump()},
        upsert=True
    )
    return {"message": "Chatbot settings successfully updated!"}

@router.post("/upload-media")
async def upload_media(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Uploads generic media images, storing them in MongoDB
    and returns the public URL.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are permitted for upload.")
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    
    try:
        content = await file.read()
        db = get_db()
        db.media_assets.update_one(
            {"filename": filename},
            {"$set": {
                "filename": filename,
                "content": content,
                "content_type": file.content_type
            }},
            upsert=True
        )
        return {"url": f"/lux_editorial/uploads/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded media: {str(e)}")

@router.post("/upload-avatar")
async def upload_avatar(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Overwrites the homepage hero avatar image file in MongoDB (manya_avatar.jpg).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image file uploads are permitted.")
    
    try:
        content = await file.read()
        db = get_db()
        db.media_assets.update_one(
            {"filename": "manya_avatar.jpg"},
            {"$set": {
                "filename": "manya_avatar.jpg",
                "content": content,
                "content_type": file.content_type
            }},
            upsert=True
        )
        return {"message": "Hero avatar successfully updated!", "url": "/lux_editorial/manya_avatar.jpg"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save avatar image: {str(e)}")

@router.post("/upload-portrait")
async def upload_portrait(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Overwrites the about me portrait image file in MongoDB (manya_portrait.jpg).
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image file uploads are permitted.")
    
    try:
        content = await file.read()
        db = get_db()
        db.media_assets.update_one(
            {"filename": "manya_portrait.jpg"},
            {"$set": {
                "filename": "manya_portrait.jpg",
                "content": content,
                "content_type": file.content_type
            }},
            upsert=True
        )
        return {"message": "About Me portrait successfully updated!", "url": "/lux_editorial/manya_portrait.jpg"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save portrait image: {str(e)}")

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), authenticated: bool = Depends(verify_admin)):
    """
    Overwrites the resume PDF document in MongoDB (resume.pdf).
    """
    if file.content_type != "application/pdf" and not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF document uploads are permitted.")
    
    try:
        content = await file.read()
        db = get_db()
        db.media_assets.update_one(
            {"filename": "resume.pdf"},
            {"$set": {
                "filename": "resume.pdf",
                "content": content,
                "content_type": "application/pdf"
            }},
            upsert=True
        )
        return {"message": "Resume PDF successfully updated!", "url": "/lux_editorial/uploads/resume.pdf"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save resume document: {str(e)}")
