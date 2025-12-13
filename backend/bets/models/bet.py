"""
Bet domain model.
"""

from datetime import datetime
from uuid import UUID
from typing_extensions import override

from backend.shared.models import DataModel

from .bet_id import BetId
from .bet_user_id import BetUserId
from .bet_coin_id import BetCoinId
from .bet_amount import BetAmount
from .bet_cost import BetCost
from .bet_status import BetStatus
from .bet_name import BetName
from .bet_create_date import BetCreatedDate
from .bet_update_date import BetUpdatedDate


class Bet(DataModel):
    """
    Bet model.

    Notes:
    - user_id = creator username (TEXT)
    - cost = coins needed to join (entry fee)
    - participants = list of usernames in this bet
    """

    __id: BetId
    __user_id: BetUserId
    __coin_id: BetCoinId
    __amount: BetAmount
    __cost: BetCost
    __status: BetStatus
    __name: BetName
    __create_date: BetCreatedDate
    __update_date: BetUpdatedDate

    # 👇 nou
    __participants: list[str]

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        user_id: str,              # ✅ ara username (TEXT)
        coin_id: str | UUID,
        amount: float,
        cost: float,               # ✅ nou
        status: str,
        name: str,
        create_date: datetime,
        update_date: datetime,
        participants: list[str] | None = None,   # ✅ nou
    ) -> None:
        self.__id = BetId(value=id)
        self.__user_id = BetUserId(value=user_id)
        self.__coin_id = BetCoinId(value=coin_id)
        self.__amount = BetAmount(value=amount)
        self.__cost = BetCost(value=cost)
        self.__status = BetStatus(value=status)
        self.__name = BetName(value=name)
        self.__create_date = BetCreatedDate(value=create_date)
        self.__update_date = BetUpdatedDate(value=update_date)
        self.__participants = participants or []

    @property
    def id(self) -> str | UUID:
        return self.__id.value

    @property
    def user_id(self) -> str:
        # creator username
        return str(self.__user_id.value)

    @property
    def coin_id(self) -> str | UUID:
        return self.__coin_id.value

    @property
    def amount(self) -> float:
        return self.__amount.value

    @amount.setter
    def amount(self, value: float) -> None:
        self.__amount = BetAmount(value=value)

    @property
    def cost(self) -> float:
        return self.__cost.value

    @cost.setter
    def cost(self, value: float) -> None:
        self.__cost = BetCost(value=value)

    @property
    def status(self) -> str:
        return self.__status.value

    @status.setter
    def status(self, value: str) -> None:
        self.__status = BetStatus(value=value)

    @property
    def name(self) -> str:
        return self.__name.value

    @name.setter
    def name(self, value: str) -> None:
        self.__name = BetName(value=value)

    @property
    def participants(self) -> list[str]:
        return self.__participants

    def add_participant(self, username: str) -> None:
        if username not in self.__participants:
            self.__participants.append(username)

    def remove_participant(self, username: str) -> None:
        if username in self.__participants:
            self.__participants.remove(username)

    @property
    def create_date(self) -> datetime:
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        return self.__update_date.value

    @update_date.setter
    def update_date(self, value: datetime) -> None:
        self.__update_date = BetUpdatedDate(value=value)
