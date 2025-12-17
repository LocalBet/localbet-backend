from backend.stats.actions.get_logged_users import get_logged_user_ids

class LoggedUsersService:
    async def get_logged_users(self) -> list[str]:
        return await get_logged_user_ids()
