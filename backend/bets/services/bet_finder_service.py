"""
Service for finding bets.
"""

from backend.shared.models import Condition, DataModel
from backend.bets.actions import BetActions
from backend.bets.models import Bet
from backend.bets.errors.errors import BetNotFoundError


class BetFinderService:
    def __init__(self, action: BetActions) -> None:
        self.__action = action

    def find(self, conditions: list[Condition[DataModel]]) -> list[Bet]:
        bets = self.__action.search(conditions)
        if not bets:
            raise BetNotFoundError(field="conditions", value=conditions)
        return bets
