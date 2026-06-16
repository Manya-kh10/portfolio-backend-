import os
from fastapi import Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

def verify_admin(request: Request):
    """
    Validates the admin session cookie against the configured password.
    """
    admin_password = os.getenv("ADMIN_PASSWORD", "manya123")
    token = request.cookies.get("admin_session")
    if token != admin_password:
        raise HTTPException(status_code=401, detail="Unauthorized: Admin session required.")
    return True

