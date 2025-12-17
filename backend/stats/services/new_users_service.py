from backend.stats.actions.get_new_users_last_24h import get_new_users_last_24h

class NewUsersService:
    async def get_new_users(self) -> list[str]:
        return await get_new_users_last_24h()
