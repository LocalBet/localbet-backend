"""
Group domain model.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING
from uuid import UUID

from backend.shared.models import DataModel

from .group_id import GroupId
from .group_name import GroupName
from .group_created_at import GroupCreatedAt
from .group_updated_at import GroupUpdatedAt
from .group_creator_id import GroupCreatorId
from .group_description import GroupDescription
from .group_is_active import GroupIsActive

if TYPE_CHECKING:
    from backend.bets.models.bet import Bet


class Group(DataModel):
    """
    Group model aligned with SQL schema v2.0.
    
    Schema reference (04_tables.sql):
    - id: UUID (PK)
    - name: VARCHAR(100)
    - description: TEXT (optional)
    - creator_id: UUID (FK to user)
    - is_active: BOOLEAN
    - created_at: TIMESTAMP
    - updated_at: TIMESTAMP
    
    Relations:
    - members: via group_member table (user_id UUID)
    - bets: via bet.group_id FK (reverse relation)
    """

    __id: GroupId
    __name: GroupName
    __description: GroupDescription
    __creator_id: GroupCreatorId
    __is_active: GroupIsActive
    __created_at: GroupCreatedAt
    __updated_at: GroupUpdatedAt

    # Hydrated relations (optional, loaded separately)
    __members: list[UUID] | None
    __bets: list["Bet"] | None

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        name: str,
        creator_id: str | UUID,
        created_at: datetime,
        updated_at: datetime,
        description: str | None = None,
        is_active: bool = True,
        # Optional hydrated relations
        members: list[UUID] | None = None,
        hydrated_bets: list["Bet"] | None = None,
    ) -> None:
        self.__id = GroupId(value=id)
        self.__name = GroupName(value=name)
        self.__description = GroupDescription(value=description)
        self.__creator_id = GroupCreatorId(value=creator_id)
        self.__is_active = GroupIsActive(value=is_active)
        self.__created_at = GroupCreatedAt(value=created_at)
        self.__updated_at = GroupUpdatedAt(value=updated_at)

        self.__members = members
        self.__bets = hydrated_bets

    @property
    def id(self) -> str | UUID:
        return self.__id.value

    @property
    def name(self) -> str:
        return self.__name.value

    @property
    def description(self) -> str | None:
        return self.__description.value

    @property
    def creator_id(self) -> UUID:
        return self.__creator_id.value

    @property
    def is_active(self) -> bool:
        return self.__is_active.value

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self.__is_active = GroupIsActive(value=value)

    @property
    def created_at(self) -> datetime:
        return self.__created_at.value

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at.value

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self.__updated_at = GroupUpdatedAt(value=value)

    @property
    def members(self) -> list[UUID]:
        """Returns list of member UUIDs (hydrated from group_member table)."""
        return self.__members or []

    def set_members(self, members: list[UUID]) -> None:
        """Set members list (hydrated from DB)."""
        self.__members = members

    @property
    def bets(self) -> list["Bet"]:
        """Returns list of Bet objects (hydrated from bet table)."""
        return self.__bets or []

    def set_bets(self, bets: list["Bet"]) -> None:
        """Set bets list (hydrated from DB)."""
        self.__bets = bets

    def to_persistence_dict(self) -> dict[str, Any]:
        """Dict for saving to PostgreSQL."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_dict(self) -> dict[str, Any]:
        """
        Dict for API response (schema GroupGetSchema).
        """
        bets_payload: list[Any] = []
        if self.__bets:
            bets_payload = [b.to_dict() for b in self.__bets]

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "creator_id": self.creator_id,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "members": [str(m) for m in self.members],  # Convert UUIDs to strings
            "bets": bets_payload,
        }
