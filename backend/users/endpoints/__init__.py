from fastapi import APIRouter

from .user_delete_endpoint import route as user_delete_endpoint
from .user_get_controller import route as user_get_endpoint
from .user_update_controller import route as user_update_endpoint
from .user_list_controller import route as user_list_endpoint
from .change_password_endpoint import route as change_password_endpoint
from .wallet_endpoints import route as wallet_endpoint

router = APIRouter()

# /users/me endpoints
router.include_router(user_get_endpoint, prefix="/me")
router.include_router(user_update_endpoint, prefix="/me")
router.include_router(user_delete_endpoint, prefix="/me")
router.include_router(change_password_endpoint, prefix="/me")

# /users/wallet endpoints
router.include_router(wallet_endpoint, prefix="/wallet")

# /users (admin only)
router.include_router(user_list_endpoint)

__all__ = ("router",)
