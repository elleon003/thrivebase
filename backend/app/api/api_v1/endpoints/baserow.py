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
        table_id = os.getenv("BASEROW_TRANSACTIONS_TABLE_ID")
        
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

@router.get("/user-transactions")
async def get_user_transactions(
    session: SessionContainer = Depends(verify_session),
    account_id: str = None
) -> List[Dict]:
    """
    Get all transactions for a user, optionally filtered by account_id
    """
    try:
        user_id = session.get_user_id()
        table_id = os.getenv("BASEROW_TRANSACTIONS_TABLE_ID")
        
        # Build query parameters
        query_params = f"user_id={user_id}"
        if account_id:
            query_params += f"&account_id={account_id}"
        
        # Query Baserow for user's transactions
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{table_id}/?{query_params}"
        )
        
        return response.get("results", [])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/account-summary")
async def get_account_summary(
    session: SessionContainer = Depends(verify_session)
) -> List[Dict]:
    """
    Get summary of all accounts for a user
    """
    try:
        user_id = session.get_user_id()
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        
        # Query Baserow for user's accounts
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}"
        )
        
        accounts = response.get("results", [])
        
        # Calculate total balances
        total_current = sum(float(account["balance_current"]) for account in accounts)
        total_available = sum(
            float(account["balance_available"]) 
            for account in accounts 
            if account["balance_available"] is not None
        )
        
        return {
            "accounts": accounts,
            "summary": {
                "total_current_balance": total_current,
                "total_available_balance": total_available,
                "total_accounts": len(accounts)
            }
        }
    
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
        
        transactions_table_id = os.getenv("BASEROW_TRANSACTIONS_TABLE_ID")
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        
        # Delete from Baserow transactions table
        await baserow_request(
            method="DELETE",
            endpoint=f"/database/rows/table/{transactions_table_id}/?user_id={user_id}"
        )
        
        # Delete from Baserow accounts table
        await baserow_request(
            method="DELETE",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}"
        )
        
        return {"status": "success", "message": "User data deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
