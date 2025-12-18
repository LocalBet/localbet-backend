from backend.stats.actions.get_new_bets_last_24h import get_new_bets_last_24h

class NewBetsService:
    async def get_new_bets(self) -> list[str]:
        return await get_new_bets_last_24h()
