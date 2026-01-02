import time
from backend.services.redis import redis_client

async def get_new_users_last_24h() -> list[str]:
    now = int(time.time())
    twenty_four_hours_ago = now - 86400  # 24h in seconds
    return await redis_client.zrangebyscore("new_users", twenty_four_hours_ago, now)
