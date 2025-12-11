from fastapi import APIRouter

from .group_create_controller import route as group_create_endpoint
from .group_get_controller import route as group_get_endpoint
from .group_list_controller import route as group_list_endpoint
from .group_user_groups_controller import route as group_user_groups_endpoint

router = APIRouter()

# /groups endpoints
router.include_router(group_create_endpoint)
router.include_router(group_get_endpoint)
router.include_router(group_list_endpoint)
router.include_router(group_user_groups_endpoint)

__all__ = ("router",)
