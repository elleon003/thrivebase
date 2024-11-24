from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
import aiohttp
import os
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from pydantic import BaseModel

router = APIRouter()

class TransactionData(BaseModel):
    account_id: str
    amount: float
    date: str
    description: str
    category: str

async def baserow_request(method: str, endpoint: str, data: Dict = None) -> Dict:
    """
    Helper function to make requests to Baserow API
    """
    base_url = os.getenv("BASEROW_API_URL")
    headers = {
        "Authorization": f"Token {os.getenv('BASEROW_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        url = f"{base_url}{endpoint}"
        async with session.request(
            method=method,
            url=url,
            headers=headers,
            json=data
        ) as response:
            if response.status >= 400:
                raise HTTPException(
                    status_code=response.status,
                    detail="Baserow API request failed"
                )
            return await response.json()

@router.post("/store-transactions")
async def store_transactions(
    transactions: List[TransactionData],
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Store transaction data in Baserow
    """
    try:
        user_id = session.get_user_id()
        table_id = os.getenv("BASEROW_TABLE_ID")
        
        # Transform transactions into Baserow format
        rows = []
        for transaction in transactions:
            rows.append({
                "user_id": user_id,
                "account_id": transaction.account_id,
                "amount": transaction.amount,
                "date": transaction.date,
                "description": transaction.description,
                "category": transaction.category
            })
        
        # Store in Baserow
        response = await baserow_request(
            method="POST",
            endpoint=f"/database/rows/table/{table_id}/batch/",
            data={"items": rows}
        )
        
        return {"status": "success", "message": f"Stored {len(transactions)} transactions"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/newsletter-signup")
async def store_newsletter_signup(email: str) -> Dict:
    """
    Store newsletter signup in Baserow
    """
    try:
        newsletter_table_id = os.getenv("BASEROW_NEWSLETTER_TABLE_ID")
        
        # Store in Baserow
        response = await baserow_request(
            method="POST",
            endpoint=f"/database/rows/table/{newsletter_table_id}/",
            data={
                "email": email,
                "signup_date": "NOW()",
                "status": "active"
            }
        )
        
        return {"status": "success", "message": "Newsletter signup stored successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-transactions")
async def get_user_transactions(
    session: SessionContainer = Depends(verify_session)
) -> List[Dict]:
    """
    Get all transactions for a user
    """
    try:
        user_id = session.get_user_id()
        table_id = os.getenv("BASEROW_TABLE_ID")
        
        # Query Baserow for user's transactions
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{table_id}/?user_id={user_id}"
        )
        
        return response.get("results", [])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user-data/{user_id}")
async def delete_user_data(
    user_id: str,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Delete all user data from Baserow (for account deletion)
    """
    try:
        # Verify the requesting user is the same as the user being deleted
        if session.get_user_id() != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        table_id = os.getenv("BASEROW_TABLE_ID")
        
        # Delete from Baserow
        response = await baserow_request(
            method="DELETE",
            endpoint=f"/database/rows/table/{table_id}/?user_id={user_id}"
        )
        
        return {"status": "success", "message": "User data deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
