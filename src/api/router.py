from fastapi import APIRouter, Depends

from helpers.authenticator import get_current_active_user
from .endpoints import items, users

api_router = APIRouter()
api_router.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_current_active_user)],
)
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
