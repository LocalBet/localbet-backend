from abc import ABC, abstractmethod
from backend.bets.models import Bet
from backend.shared.models import Condition, DataModel


class BetActions(ABC):
    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[Bet]:
        ...

    @abstractmethod
    def save(self, bet: Bet) -> None:
        ...

    @abstractmethod
    def update(self, bet: Bet) -> None:
        ...

    @abstractmethod
    def delete(self, bet: Bet) -> None:
        ...
