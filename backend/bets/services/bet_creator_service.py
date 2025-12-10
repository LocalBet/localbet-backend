"""
Service for creating bets.
"""

from backend.bets.actions import BetActions
from backend.bets.models import Bet


class BetCreatorService:
    def __init__(self, action: BetActions) -> None:
        self.__action = action

    def create(self, bet: Bet) -> None:
        self.__action.save(bet)
