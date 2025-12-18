import time
from backend.services.redis import redis_client

async def get_new_bets_last_24h() -> list[str]:
    now = int(time.time())
    twenty_four_hours_ago = now - 86400
    # Bets stored in ZSET "new_bets" with score = created_at timestamp
    return await redis_client.zrangebyscore("new_bets", twenty_four_hours_ago, now)
