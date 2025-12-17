from fastapi import APIRouter
from .logged_users_controller import route as logged_users_router
from .new_last_users_24h_controller import route as new_users_router

router = APIRouter()

router.include_router(logged_users_router, prefix="/logged-user")
router.include_router(new_users_router, prefix="/new-users-last-24h")