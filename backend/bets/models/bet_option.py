"""
BetOption domain model.
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing_extensions import override

from backend.shared.models import DataModel


class BetOption(DataModel):
    """
    BetOption model representing an available option for a bet.
    Example: "Resultado: 2-1" with value "100" (cuota/multiplicador).
    """
    __id: UUID
    __bet_id: UUID
    __option_name: str
    __option_value: str
    __created_at: datetime

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        *,
        id: UUID | None = None,
        bet_id: UUID,
        option_name: str,
        option_value: str,
        created_at: datetime | None = None,
    ) -> None:
        """
        BetOption domain model constructor.

        Args:
            id (UUID | None): Bet option ID (generated if None).
            bet_id (UUID): ID of the bet this option belongs to.
            option_name (str): Name of the option (e.g., "Resultado: 2-1").
            option_value (str): Value/cuota as string (e.g., "100").
            created_at (datetime | None): Creation timestamp.
        """
        self.__id = id or uuid4()
        self.__bet_id = bet_id
        self.__option_name = option_name
        self.__option_value = option_value
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
    def bet_id(self) -> UUID:
        return self.__bet_id

    @property
    def option_name(self) -> str:
        return self.__option_name

    @option_name.setter
    def option_name(self, value: str) -> None:
        self.__option_name = value

    @property
    def option_value(self) -> str:
        return self.__option_value

    @option_value.setter
    def option_value(self, value: str) -> None:
        self.__option_value = value

    @property
    def created_at(self) -> datetime:
        return self.__created_at
