from fastapi import APIRouter
from .logged_users_controller import route as logged_users_router
from .new_last_users_24h_controller import route as new_users_router
from .new_last_bets_24h_controller import route as new_bets_router
from .system_stats_controller import route as system_stats_router

router = APIRouter()

router.include_router(logged_users_router, prefix="/logged-user")
router.include_router(new_users_router, prefix="/new-users-last-24h")
router.include_router(new_bets_router, prefix="/new-bets-last-24h")
router.include_router(system_stats_router, prefix="/system-stats")