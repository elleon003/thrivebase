from fastapi import APIRouter
from app.api.api_v1.endpoints import plaid, users, baserow

api_router = APIRouter()

# Include specific endpoint routers
api_router.include_router(
    plaid.router,
    prefix="/plaid",
    tags=["plaid"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    baserow.router,
    prefix="/baserow",
    tags=["baserow"]
)
