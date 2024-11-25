from fastapi import APIRouter, Depends, HTTPException
from plaid import Client as PlaidClient
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
import os
from typing import Dict, List
from datetime import datetime
from decimal import Decimal
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from ..endpoints.baserow import baserow_request
from ....models.account import AccountCreate, AccountUpdate
from ....services.token_service import token_service

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
    Exchange public token for access token and item ID, then store account information
    """
    try:
        user_id = session.get_user_id()
        
        # Exchange public token for access token
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response["access_token"]
        item_id = exchange_response["item_id"]
        
        # Get institution information
        item_response = plaid_client.item_get(access_token)
        institution_id = item_response['item']['institution_id']
        
        institution_request = InstitutionsGetByIdRequest(
            institution_id=institution_id,
            country_codes=[CountryCode('US')]
        )
        institution_response = plaid_client.institutions_get_by_id(institution_request)
        institution_name = institution_response['institution']['name']
        
        # Store encrypted access token
        await token_service.store_token(
            access_token=access_token,
            item_id=item_id,
            user_id=user_id,
            institution_id=institution_id,
            institution_name=institution_name
        )
        
        # Get account information
        accounts_request = AccountsGetRequest(
            access_token=access_token
        )
        accounts_response = plaid_client.accounts_get(accounts_request)
        
        # Store accounts in Baserow
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        for account in accounts_response["accounts"]:
            account_data = AccountCreate(
                plaid_account_id=account["account_id"],
                plaid_item_id=item_id,
                name=account["name"],
                official_name=account.get("official_name"),
                type=account["type"],
                subtype=account.get("subtype"),
                balance_current=Decimal(str(account["balances"]["current"])) if account["balances"]["current"] is not None else Decimal("0"),
                balance_available=Decimal(str(account["balances"]["available"])) if account["balances"]["available"] is not None else None,
                iso_currency_code=account["balances"]["iso_currency_code"],
                user_id=user_id
            )
            
            await baserow_request(
                method="POST",
                endpoint=f"/database/rows/table/{accounts_table_id}/",
                data=account_data.dict()
            )
        
        return {
            "item_id": item_id,
            "institution_name": institution_name,
            "accounts_added": len(accounts_response["accounts"])
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accounts")
async def get_accounts(session: SessionContainer = Depends(verify_session)) -> List:
    """
    Get all accounts associated with the user
    """
    try:
        user_id = session.get_user_id()
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        
        # Query Baserow for user's accounts
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}"
        )
        
        return response.get("results", [])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/accounts/update/{plaid_item_id}")
async def update_accounts(
    plaid_item_id: str,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Update account balances for a specific item
    """
    try:
        user_id = session.get_user_id()
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        
        # Get access token
        access_token = await token_service.get_access_token(plaid_item_id, user_id)
        if not access_token:
            raise HTTPException(status_code=404, detail="Access token not found")
        
        # Get current accounts from Baserow
        current_accounts = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}&plaid_item_id={plaid_item_id}"
        )
        
        # Get fresh account data from Plaid
        accounts_request = AccountsGetRequest(
            access_token=access_token
        )
        plaid_accounts = plaid_client.accounts_get(accounts_request)
        
        # Update each account
        for account in current_accounts.get("results", []):
            plaid_account = next(
                (a for a in plaid_accounts["accounts"] if a["account_id"] == account["plaid_account_id"]),
                None
            )
            
            if plaid_account:
                update_data = AccountUpdate(
                    balance_current=Decimal(str(plaid_account["balances"]["current"])) if plaid_account["balances"]["current"] is not None else Decimal("0"),
                    balance_available=Decimal(str(plaid_account["balances"]["available"])) if plaid_account["balances"]["available"] is not None else None,
                    last_updated=datetime.utcnow()
                )
                
                await baserow_request(
                    method="PATCH",
                    endpoint=f"/database/rows/table/{accounts_table_id}/{account['id']}/",
                    data=update_data.dict()
                )
        
        return {"status": "success", "message": "Accounts updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/disconnect/{item_id}")
async def disconnect_account(
    item_id: str,
    session: SessionContainer = Depends(verify_session)
) -> Dict:
    """
    Disconnect a bank account and remove associated accounts
    """
    try:
        user_id = session.get_user_id()
        accounts_table_id = os.getenv("BASEROW_ACCOUNTS_TABLE_ID")
        
        # Get access token and revoke it
        access_token = await token_service.get_access_token(item_id, user_id)
        if access_token:
            # Remove item from Plaid
            plaid_client.item_remove(access_token)
            # Revoke token in our storage
            await token_service.revoke_token(item_id, user_id)
        
        # Delete accounts from Baserow
        await baserow_request(
            method="DELETE",
            endpoint=f"/database/rows/table/{accounts_table_id}/?user_id={user_id}&plaid_item_id={item_id}"
        )
        
        return {"status": "success", "message": "Account disconnected successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/connected-institutions")
async def get_connected_institutions(
    session: SessionContainer = Depends(verify_session)
) -> List[Dict]:
    """
    Get a list of all connected financial institutions for the user
    """
    try:
        user_id = session.get_user_id()
        tokens = await token_service.get_user_tokens(user_id)
        
        return [{
            "item_id": token["plaid_item_id"],
            "institution_name": token["institution_name"],
            "institution_id": token["institution_id"],
            "status": token["status"]
        } for token in tokens]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
