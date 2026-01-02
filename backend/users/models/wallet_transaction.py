"""
WalletTransaction domain model.
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing_extensions import override

from backend.shared.models import DataModel


class WalletTransaction(DataModel):
    """
    WalletTransaction model representing a wallet movement (credit/debit).
    Used for transaction history in WalletScreen.
    """
    __id: UUID
    __user_id: UUID
    __amount: int  # Positive = credit, Negative = debit
    __transaction_type: str
    __reference_id: UUID | None
    __description: str | None
    __created_at: datetime

    __hash__ = DataModel.__hash__

    # Valid transaction types
    VALID_TYPES = {
        'initial_balance',
        'bet_placed',
        'bet_won',
        'bet_lost',
        'purchase',
        'minigame_win',
        'minigame_loss',
    }

    def __init__(
        self,
        *,
        id: UUID | None = None,
        user_id: UUID,
        amount: int,
        transaction_type: str,
        reference_id: UUID | None = None,
        description: str | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """
        WalletTransaction domain model constructor.

        Args:
            id (UUID | None): Transaction ID (generated if None).
            user_id (UUID): ID of the user.
            amount (int): Amount (positive=credit, negative=debit).
            transaction_type (str): Type of transaction (see VALID_TYPES).
            reference_id (UUID | None): Optional FK to bet_id, user_bet_id, etc.
            description (str | None): Human-readable description.
            created_at (datetime | None): Creation timestamp.
        
        Raises:
            ValueError: If transaction_type is not valid.
        """
        if transaction_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid transaction type: {transaction_type}. "
                f"Must be one of: {', '.join(self.VALID_TYPES)}"
            )

        self.__id = id or uuid4()
        self.__user_id = user_id
        self.__amount = amount
        self.__transaction_type = transaction_type
        self.__reference_id = reference_id
        self.__description = description
        self.__created_at = created_at or datetime.now()

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def user_id(self) -> UUID:
        return self.__user_id

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def transaction_type(self) -> str:
        return self.__transaction_type

    @property
    def reference_id(self) -> UUID | None:
        return self.__reference_id

    @property
    def description(self) -> str | None:
        return self.__description

    @description.setter
    def description(self, value: str | None) -> None:
        self.__description = value

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    def is_credit(self) -> bool:
        """Check if this is a credit transaction (positive amount)."""
        return self.__amount > 0

    def is_debit(self) -> bool:
        """Check if this is a debit transaction (negative amount)."""
        return self.__amount < 0
