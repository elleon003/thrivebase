from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.emailpassword.asyncio import update_email_or_password
from supertokens_python.recipe.thirdpartyemailpassword.asyncio import get_user_by_id
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UpdateProfileRequest(BaseModel):
    email: EmailStr | None = None
    current_password: str | None = None
    new_password: str | None = None

@router.get("/me")
async def get_user_profile(session: SessionContainer = Depends(verify_session)) -> Dict:
    """
    Get the current user's profile information
    """
    try:
        user_id = session.get_user_id()
        user = await get_user_by_id(user_id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user_id,
            "email": user.email,
            "time_joined": user.time_joined,
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile")
async def update_profile(
    update_data: UpdateProfileRequest,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Update user profile information (email and/or password)
    """
    try:
        user_id = session.get_user_id()
        
        if update_data.email or update_data.new_password:
            # Update email and/or password using SuperTokens
            await update_email_or_password(
                user_id=user_id,
                email=update_data.email,
                password=update_data.new_password,
                current_password=update_data.current_password
            )
        
        return {"status": "success", "message": "Profile updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/connected-accounts")
async def get_connected_accounts(session: SessionContainer = Depends(verify_session)) -> Dict:
    """
    Get all connected bank accounts for the user
    """
    try:
        user_id = session.get_user_id()
        
        # Here you would typically fetch the user's connected accounts from your database
        # For now, returning a placeholder response
        return {
            "accounts": []
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/newsletter-signup")
async def newsletter_signup(email: EmailStr) -> Dict:
    """
    Sign up for the newsletter (pre-launch)
    """
    try:
        # Here you would typically:
        # 1. Validate the email
        # 2. Store it in Baserow
        # 3. Send a confirmation email
        
        return {
            "status": "success",
            "message": "Thank you for signing up! We'll keep you updated on our launch."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
