from fastapi import APIRouter, Depends, HTTPException
from plaid import Client as PlaidClient
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import os
from typing import Dict, List
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer

router = APIRouter()

# Initialize Plaid client
plaid_client = PlaidClient(
    client_id=os.getenv("PLAID_CLIENT_ID"),
    secret=os.getenv("PLAID_SECRET"),
    environment=os.getenv("PLAID_ENV", "sandbox")
)

@router.post("/create_link_token")
async def create_link_token(session: SessionContainer = Depends(verify_session)) -> Dict:
    """
    Create a link token for Plaid Link initialization
    """
    try:
        user_id = session.get_user_id()
        
        request = LinkTokenCreateRequest(
            products=[Products("transactions")],
            client_name="ThriveBase",
            country_codes=[CountryCode("US")],
            language="en",
            user=LinkTokenCreateRequestUser(
                client_user_id=user_id
            )
        )
        
        response = plaid_client.link_token_create(request)
        return {"link_token": response["link_token"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/exchange_public_token")
async def exchange_public_token(
    public_token: str,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Exchange public token for access token and item ID
    """
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        response = plaid_client.item_public_token_exchange(exchange_request)
        
        # Here you would typically store the access_token and item_id in your database
        # associated with the user_id from the session
        
        return {
            "access_token": response["access_token"],
            "item_id": response["item_id"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accounts")
async def get_accounts(session: SessionContainer = Depends(verify_session)) -> List:
    """
    Get all accounts associated with the user
    """
    try:
        # Here you would typically retrieve the user's access tokens from your database
        # and use them to fetch account information
        
        # Placeholder response
        return []
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/disconnect/{item_id}")
async def disconnect_account(
    item_id: str,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Disconnect a bank account
    """
    try:
        # Here you would typically remove the access token and item_id from your database
        # and remove the item from Plaid
        
        return {"status": "success", "message": "Account disconnected successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
