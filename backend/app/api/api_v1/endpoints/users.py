from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.emailpassword.asyncio import update_email_or_password
from supertokens_python.recipe.thirdpartyemailpassword.asyncio import get_user_by_id
from pydantic import BaseModel, EmailStr
from ..endpoints.baserow import baserow_request
import os
from datetime import datetime

router = APIRouter()

class UpdateProfileRequest(BaseModel):
    email: EmailStr | None = None
    current_password: str | None = None
    new_password: str | None = None

class NewsletterSignup(BaseModel):
    email: EmailStr
    signup_date: datetime = datetime.utcnow()
    status: str = "active"

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
    Get all connected bank accounts for the user with their balances and institutions
    """
    try:
        user_id = session.get_user_id()
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        tokens_table_id = os.getenv("BASEROW_TOKENS_TABLE_ID")
        
        # Get user's accounts
        accounts_response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}"
        )
        
        # Get institution information
        tokens_response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{tokens_table_id}/?user_id={user_id}&status=active"
        )
        
        # Create a map of item_id to institution info
        institution_map = {
            token["plaid_item_id"]: {
                "institution_name": token["institution_name"],
                "institution_id": token["institution_id"]
            }
            for token in tokens_response.get("results", [])
        }
        
        # Group accounts by institution
        accounts_by_institution = {}
        for account in accounts_response.get("results", []):
            item_id = account["plaid_item_id"]
            institution_info = institution_map.get(item_id, {})
            
            if institution_info.get("institution_name") not in accounts_by_institution:
                accounts_by_institution[institution_info.get("institution_name", "Unknown")] = {
                    "institution_id": institution_info.get("institution_id"),
                    "accounts": []
                }
            
            accounts_by_institution[institution_info.get("institution_name", "Unknown")]["accounts"].append({
                "id": account["id"],
                "name": account["name"],
                "type": account["type"],
                "subtype": account["subtype"],
                "balance_current": float(account["balance_current"]),
                "balance_available": float(account["balance_available"]) if account["balance_available"] else None,
                "currency": account["iso_currency_code"]
            })
        
        return {
            "institutions": [
                {
                    "name": institution_name,
                    "institution_id": info["institution_id"],
                    "accounts": info["accounts"]
                }
                for institution_name, info in accounts_by_institution.items()
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/newsletter-signup")
async def newsletter_signup(email: EmailStr) -> Dict:
    """
    Sign up for the newsletter (pre-launch)
    """
    try:
        newsletter_table_id = os.getenv("BASEROW_NEWSLETTER_TABLE_ID")
        if not newsletter_table_id:
            raise HTTPException(
                status_code=500,
                detail="Newsletter table ID not configured"
            )
        
        # Check if email already exists
        existing = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{newsletter_table_id}/?email={email}"
        )
        
        if existing.get("results"):
            return {
                "status": "success",
                "message": "You're already signed up for our newsletter!"
            }
        
        # Create new signup
        signup_data = NewsletterSignup(email=email)
        
        await baserow_request(
            method="POST",
            endpoint=f"/database/rows/table/{newsletter_table_id}/",
            data=signup_data.dict()
        )
        
        return {
            "status": "success",
            "message": "Thank you for signing up! We'll keep you updated on our launch."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
