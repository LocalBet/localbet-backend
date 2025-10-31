
from fastapi import APIRouter

from .refresh_access_token_endpoint import route as refresh_access_token_endpoint
from .user_login_endpoint import route as user_login_endpoint
from .user_register_endpoint import route as user_register_endpoint

router = APIRouter()
router.include_router(router=user_login_endpoint)
router.include_router(router=user_register_endpoint)
router.include_router(router=refresh_access_token_endpoint)

__all__ = ('router',)
