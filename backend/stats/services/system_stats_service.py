from backend.stats.actions.system_stats_actions import SystemStatsActions

class SystemStatsService:
    def __init__(self, actions: SystemStatsActions):
        self.actions = actions

    async def get_system_stats(self) -> dict:
        return self.actions.get_stats()