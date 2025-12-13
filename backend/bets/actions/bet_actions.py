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

    # ✅ join dins d'un grup (validació group_bet + cobrar + amount += cost)
    @abstractmethod
    def join_bet_in_group(self, group_id: str, bet_id: str, username: str) -> None:
        ...

    @abstractmethod
    def leave_bet(self, bet_id: str, username: str) -> None:
        ...
