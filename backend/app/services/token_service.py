from datetime import datetime
from typing import Optional, Dict
from ..core.security import token_encryption
from ..models.token import PlaidTokenCreate, PlaidTokenUpdate
from ..api.api_v1.endpoints.baserow import baserow_request
import os

class TokenService:
    def __init__(self):
        self.table_id = os.getenv("BASEROW_TOKENS_TABLE_ID")
        if not self.table_id:
            raise ValueError("BASEROW_TOKENS_TABLE_ID environment variable is required")

    async def store_token(
        self,
        access_token: str,
        item_id: str,
        user_id: str,
        institution_id: Optional[str] = None,
        institution_name: Optional[str] = None
    ) -> Dict:
        """
        Store an encrypted access token in Baserow
        """
        encrypted_token = token_encryption.encrypt_token(access_token)
        
        token_data = PlaidTokenCreate(
            plaid_item_id=item_id,
            encrypted_access_token=encrypted_token,
            user_id=user_id,
            institution_id=institution_id,
            institution_name=institution_name,
            status="active"
        )
        
        response = await baserow_request(
            method="POST",
            endpoint=f"/database/rows/table/{self.table_id}/",
            data=token_data.dict()
        )
        
        return response

    async def get_access_token(self, item_id: str, user_id: str) -> Optional[str]:
        """
        Retrieve and decrypt an access token from Baserow
        """
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{self.table_id}/?user_id={user_id}&plaid_item_id={item_id}&status=active"
        )
        
        results = response.get("results", [])
        if not results:
            return None
            
        encrypted_token = results[0].get("encrypted_access_token")
        return token_encryption.decrypt_token(encrypted_token)

    async def revoke_token(self, item_id: str, user_id: str) -> bool:
        """
        Mark a token as revoked in Baserow
        """
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{self.table_id}/?user_id={user_id}&plaid_item_id={item_id}&status=active"
        )
        
        results = response.get("results", [])
        if not results:
            return False
            
        token_id = results[0].get("id")
        update_data = PlaidTokenUpdate(
            status="revoked",
            last_updated=datetime.utcnow()
        )
        
        await baserow_request(
            method="PATCH",
            endpoint=f"/database/rows/table/{self.table_id}/{token_id}/",
            data=update_data.dict()
        )
        
        return True

    async def get_user_tokens(self, user_id: str) -> list:
        """
        Get all active tokens for a user
        """
        response = await baserow_request(
            method="GET",
            endpoint=f"/database/rows/table/{self.table_id}/?user_id={user_id}&status=active"
        )
        
        return response.get("results", [])

    async def delete_user_tokens(self, user_id: str) -> bool:
        """
        Delete all tokens for a user (used during account deletion)
        """
        await baserow_request(
            method="DELETE",
            endpoint=f"/database/rows/table/{self.table_id}/?user_id={user_id}"
        )
        
        return True

# Global instance
token_service = TokenService()
