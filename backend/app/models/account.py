from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class AccountBase(BaseModel):
    plaid_account_id: str
    plaid_item_id: str
    name: str
    official_name: Optional[str]
    type: str
    subtype: Optional[str]
    balance_current: Decimal
    balance_available: Optional[Decimal]
    iso_currency_code: str
    user_id: str

class AccountCreate(AccountBase):
    """
    Account creation model that inherits all fields from AccountBase.
    No additional fields are needed for account creation.
    """
    pass

class AccountInDB(AccountBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True

class AccountUpdate(BaseModel):
    balance_current: Decimal
    balance_available: Optional[Decimal]
    last_updated: datetime
