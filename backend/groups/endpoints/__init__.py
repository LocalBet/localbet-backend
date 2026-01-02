from fastapi import APIRouter

from .group_create_controller import route as group_create_endpoint
from .group_get_controller import route as group_get_endpoint
from .group_list_controller import route as group_list_endpoint
from .group_user_groups_controller import route as group_user_groups_endpoint
from .group_join_controller import route as group_join_endpoint
from .group_create_bet_controller import route as group_create_bet_endpoint  # ✅ nou
from .group_bet_join_controller import route as group_bet_join_endpoint
from .group_bet_resolve_controller import route as group_bet_resolve_endpoint




router = APIRouter()

# /groups endpoints
router.include_router(group_create_endpoint)
router.include_router(group_get_endpoint)
router.include_router(group_list_endpoint)
router.include_router(group_user_groups_endpoint)
router.include_router(group_join_endpoint)
router.include_router(group_create_bet_endpoint)  # ✅ nou: POST /{group_id}/bets
router.include_router(group_bet_join_endpoint)
router.include_router(group_bet_resolve_endpoint)

__all__ = ("router",)
