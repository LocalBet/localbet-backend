from fastapi import APIRouter

from .bet_create_controller import route as bet_create_endpoint
from .bet_get_controller import route as bet_get_endpoint
from .bet_list_controller import route as bet_list_endpoint
# ✅ nou

router = APIRouter()

# /bets endpoints
router.include_router(bet_create_endpoint)
router.include_router(bet_get_endpoint)
router.include_router(bet_list_endpoint)


__all__ = ("router",)
