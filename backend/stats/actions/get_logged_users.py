import time
from backend.services.redis import redis_client

async def get_logged_user_ids() -> list[str]:
    now = int(time.time())
    await redis_client.zremrangebyscore("active_users", 0, now)
    active = await redis_client.zrangebyscore("active_users", now, "+inf")
    return active
