
from fastapi import APIRouter

from .user_delete_endpoint import route as user_delete_endpoint
from .user_get_controller import route as user_get_endpoint
from .user_update_controller import route as user_update_endpoint

router = APIRouter(prefix='/me')
router.include_router(router=user_get_endpoint)
router.include_router(router=user_update_endpoint)
router.include_router(router=user_delete_endpoint)

__all__ = ('router',)
