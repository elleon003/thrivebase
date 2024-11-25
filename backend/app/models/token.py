from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PlaidTokenBase(BaseModel):
    plaid_item_id: str
    encrypted_access_token: str
    user_id: str
    institution_id: Optional[str]
    institution_name: Optional[str]
    status: str = "active"  # active, revoked, error

class PlaidTokenCreate(PlaidTokenBase):
    """
    Token creation model that inherits all fields from PlaidTokenBase.
    No additional fields are needed for token creation as all necessary
    fields are defined in the base model.
    """
    pass

class PlaidTokenInDB(PlaidTokenBase):
    id: int
    created_at: datetime
    last_updated: datetime

    class Config:
        orm_mode = True

class PlaidTokenUpdate(BaseModel):
    status: Optional[str]
    last_updated: datetime
