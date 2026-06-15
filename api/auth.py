import os
from fastapi import Request, HTTPException

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "manya123")

def verify_admin(request: Request):
    """
    Validates the admin session cookie against the configured password.
    """
    token = request.cookies.get("admin_session")
    if token != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized: Admin session required.")
    return True
