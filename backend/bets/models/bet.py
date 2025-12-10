"""
Bet domain model.
"""

from datetime import datetime
from typing_extensions import override
from uuid import UUID

from backend.shared.models import DataModel

from .bet_id import BetId
from .bet_user_id import BetUserId
from .bet_coin_id import BetCoinId
from .bet_amount import BetAmount
from .bet_status import BetStatus
from .bet_name import BetName
from .bet_create_date import BetCreatedDate
from .bet_update_date import BetUpdatedDate


class Bet(DataModel):
    """
    Bet model.
    """

    __id: BetId
    __user_id: BetUserId
    __coin_id: BetCoinId
    __amount: BetAmount
    __status: BetStatus
    __name: BetName
    __create_date: BetCreatedDate
    __update_date: BetUpdatedDate

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        user_id: str | UUID,
        coin_id: str | UUID,
        amount: float,
        status: str,
        name: str,
        create_date: datetime,
        update_date: datetime,
    ) -> None:
        self.__id = BetId(value=id)
        self.__user_id = BetUserId(value=user_id)
        self.__coin_id = BetCoinId(value=coin_id)
        self.__amount = BetAmount(value=amount)
        self.__status = BetStatus(value=status)
        self.__name = BetName(value=name)
        self.__create_date = BetCreatedDate(value=create_date)
        self.__update_date = BetUpdatedDate(value=update_date)

    @property
    def id(self) -> str | UUID:
        return self.__id.value

    @property
    def user_id(self) -> str | UUID:
        return self.__user_id.value

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
    def create_date(self) -> datetime:
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        return self.__update_date.value

    @update_date.setter
    def update_date(self, value: datetime) -> None:
        self.__update_date = BetUpdatedDate(value=value)
