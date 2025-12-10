from backend.bets.actions import BetActions
from backend.bets.models import Bet
from backend.shared.models import Condition, DataModel


class BetService:
    def __init__(self, action: BetActions) -> None:
        self.__action = action

    def create(self, bet: Bet) -> None:
        self.__action.save(bet)

    def list(self, conditions: list[Condition[DataModel]]) -> list[Bet]:
        return self.__action.search(conditions)

    def update(self, bet: Bet) -> None:
        self.__action.update(bet)

    def delete(self, bet: Bet) -> None:
        self.__action.delete(bet)
