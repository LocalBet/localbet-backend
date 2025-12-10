from fastapi import APIRouter

from .bet_create_controller import route as bet_create_endpoint
from .bet_get_controller import route as bet_get_endpoint
from .bet_list_controller import route as bet_list_endpoint 
# later you can add bet_update_controller, bet_delete_controller

router = APIRouter()

# /bets endpoints
router.include_router(bet_create_endpoint)
router.include_router(bet_get_endpoint)
router.include_router(bet_list_endpoint)

# if you add update/delete/list, you’ll include them here too:
# router.include_router(bet_update_endpoint, prefix="/bets")
# router.include_router(bet_delete_endpoint, prefix="/bets")

__all__ = ("router",)
