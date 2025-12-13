from backend.bets.actions import BetActions
from backend.shared.infrastructure.connections import PostgreSqlConnection


class BetParticipationService:
    def __init__(self, action: BetActions, connection: PostgreSqlConnection) -> None:
        self.__action = action
        self.__connection = connection

    def join(self, bet_id: str, username: str) -> None:
        """
        Join a bet:
        - charge user coins (bet.cost)
        - insert bet_participant
        """
        self.__action.join_bet(bet_id=bet_id, username=username)
