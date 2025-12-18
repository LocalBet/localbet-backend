"""
User list controller module with Redis caching.
"""

import json
from typing import List

from fastapi import APIRouter, Request, status, Query, HTTPException
from fastapi.encoders import jsonable_encoder   # <-- add this import

from backend.auth.middlewares import UserMustBeLoggedMiddleware
from backend.database import get_database_connection
from backend.shared.infrastructure import MiddlewareWrapper
from backend.users.actions import PostgreSQLUserActions
from backend.users.services.user_finder_service import UserFinderService
from backend.users.errors import UserNotFoundError
from backend.users.schemas import UserGetSchema
from backend.services.redis import redis_client

route = APIRouter(route_class=MiddlewareWrapper(middlewares=[UserMustBeLoggedMiddleware]))


@route.get(
    path="/",
    summary="Get all users (admin only).",
    description="Allows administrators to retrieve all registered users with pagination.",
    response_model=List[UserGetSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    request: Request,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> List[UserGetSchema]:
    """
    Retrieve all users from the database, with Redis caching.
    """
    cache_key = f"users:{limit}:{offset}"
    cached = await redis_client.get(cache_key)

    if cached:
        # reconstruct Pydantic models from cached JSON
        return [UserGetSchema(**u) for u in json.loads(cached)]

    with get_database_connection() as database_connection:
        actions = PostgreSQLUserActions(connection=database_connection)
        service = UserFinderService(action=actions)

        try:
            users = service.find([])  # empty conditions → all users
        except UserNotFoundError:
            raise HTTPException(status_code=404, detail="No users found")

        paginated = users[offset : offset + limit]
        result = [UserGetSchema(**u.to_dict()) for u in paginated]

    # Safely encode datetimes/dates before caching
    encoded = jsonable_encoder(result)
    await redis_client.set(cache_key, json.dumps(encoded), ex=60)

    return result
