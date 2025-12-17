"""
Bet domain model.
"""

from datetime import datetime
from uuid import UUID
from typing_extensions import override

from backend.shared.models import DataModel

from .bet_id import BetId
from .bet_title import BetTitle
from .bet_description import BetDescription
from .bet_group_id import BetGroupId
from .bet_created_by import BetCreatedBy
from .bet_min_bet import BetMinBet
from .bet_status import BetStatus
from .bet_image_url import BetImageUrl
from .bet_deadline import BetDeadline
from .bet_created_at import BetCreatedAt
from .bet_updated_at import BetUpdatedAt


class Bet(DataModel):
    """
    Bet model aligned with SQL schema v2.0.
    
    Schema reference (04_tables.sql):
    - id: UUID (PK)
    - group_id: UUID (FK to group) - MANDATORY
    - title: VARCHAR(255)
    - description: TEXT
    - image_url: VARCHAR(500) (optional)
    - min_bet: INTEGER (default 100)
    - deadline: TIMESTAMP
    - status: VARCHAR(20) (active, closed, resolved)
    - winning_option: UUID (FK to bet_options, nullable)
    - created_by: UUID (FK to user)
    - created_at: TIMESTAMP
    - updated_at: TIMESTAMP
    
    Relations:
    - participants: via user_bets table
    - options: via bet_options table
    """

    __id: BetId
    __group_id: BetGroupId
    __title: BetTitle
    __description: BetDescription
    __image_url: BetImageUrl
    __min_bet: BetMinBet
    __deadline: BetDeadline
    __status: BetStatus
    __created_by: BetCreatedBy
    __created_at: BetCreatedAt
    __updated_at: BetUpdatedAt

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        group_id: str | UUID,
        title: str,
        description: str,
        min_bet: int,
        deadline: datetime,
        created_by: str | UUID,
        status: str,
        created_at: datetime,
        updated_at: datetime,
        image_url: str | None = None,
    ) -> None:
        self.__id = BetId(value=id)
        self.__group_id = BetGroupId(value=group_id)
        self.__title = BetTitle(value=title)
        self.__description = BetDescription(value=description)
        self.__image_url = BetImageUrl(value=image_url)
        self.__min_bet = BetMinBet(value=min_bet)
        self.__deadline = BetDeadline(value=deadline)
        self.__status = BetStatus(value=status)
        self.__created_by = BetCreatedBy(value=created_by)
        self.__created_at = BetCreatedAt(value=created_at)
        self.__updated_at = BetUpdatedAt(value=updated_at)

    @property
    def id(self) -> str | UUID:
        return self.__id.value

    @property
    def group_id(self) -> UUID:
        return self.__group_id.value

    @property
    def title(self) -> str:
        return self.__title.value

    @title.setter
    def title(self, value: str) -> None:
        self.__title = BetTitle(value=value)

    @property
    def description(self) -> str:
        return self.__description.value

    @description.setter
    def description(self, value: str) -> None:
        self.__description = BetDescription(value=value)

    @property
    def image_url(self) -> str | None:
        return self.__image_url.value

    @image_url.setter
    def image_url(self, value: str | None) -> None:
        self.__image_url = BetImageUrl(value=value)

    @property
    def min_bet(self) -> int:
        return self.__min_bet.value

    @min_bet.setter
    def min_bet(self, value: int) -> None:
        self.__min_bet = BetMinBet(value=value)

    @property
    def deadline(self) -> datetime:
        return self.__deadline.value

    @deadline.setter
    def deadline(self, value: datetime) -> None:
        self.__deadline = BetDeadline(value=value)

    @property
    def status(self) -> str:
        return self.__status.value

    @status.setter
    def status(self, value: str) -> None:
        self.__status = BetStatus(value=value)

    @property
    def created_by(self) -> UUID:
        """Creator user UUID."""
        return self.__created_by.value

    @property
    def created_at(self) -> datetime:
        return self.__created_at.value

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at.value

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self.__updated_at = BetUpdatedAt(value=value)

    def to_dict(self) -> dict:
        """Dict for API response."""
        return {
            "id": str(self.id),
            "group_id": str(self.group_id),
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "min_bet": self.min_bet,
            "deadline": self.deadline,
            "status": self.status,
            "created_by": str(self.created_by),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
