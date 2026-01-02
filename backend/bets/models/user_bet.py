"""
UserBet domain model.
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing_extensions import override

from backend.shared.models import DataModel


class UserBet(DataModel):
    """
    UserBet model representing a user's participation in a bet.
    A user can only place one bet per bet (UNIQUE constraint).
    """
    __id: UUID
    __bet_id: UUID
    __user_id: UUID
    __option_id: UUID
    __amount: int
    __placed_at: datetime
    __result: str | None  # 'won', 'lost', or NULL (pending)

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        *,
        id: UUID | None = None,
        bet_id: UUID,
        user_id: UUID,
        option_id: UUID,
        amount: int,
        placed_at: datetime | None = None,
        result: str | None = None,
    ) -> None:
        """
        UserBet domain model constructor.

        Args:
            id (UUID | None): User bet ID (generated if None).
            bet_id (UUID): ID of the bet.
            user_id (UUID): ID of the user placing the bet.
            option_id (UUID): ID of the chosen option.
            amount (int): Amount of coins bet.
            placed_at (datetime | None): Timestamp when bet was placed.
            result (str | None): Result ('won', 'lost', or None for pending).
        """
        self.__id = id or uuid4()
        self.__bet_id = bet_id
        self.__user_id = user_id
        self.__option_id = option_id
        self.__amount = amount
        self.__placed_at = placed_at or datetime.now()
        self.__result = result

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def bet_id(self) -> UUID:
        return self.__bet_id

    @property
    def user_id(self) -> UUID:
        return self.__user_id

    @property
    def option_id(self) -> UUID:
        return self.__option_id

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def placed_at(self) -> datetime:
        return self.__placed_at

    @property
    def result(self) -> str | None:
        return self.__result

    @result.setter
    def result(self, value: str | None) -> None:
        """Set result to 'won', 'lost', or None."""
        if value not in ('won', 'lost', None):
            raise ValueError(f"Invalid result: {value}. Must be 'won', 'lost', or None.")
        self.__result = value

    def mark_as_won(self) -> None:
        """Mark this bet as won."""
        self.__result = 'won'

    def mark_as_lost(self) -> None:
        """Mark this bet as lost."""
        self.__result = 'lost'

    def is_pending(self) -> bool:
        """Check if bet result is still pending."""
        return self.__result is None
