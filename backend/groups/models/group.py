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
from .group_create_date import GroupCreateDate
from .group_update_date import GroupUpdateDate

if TYPE_CHECKING:
    # Ajusta l'import segons la teva estructura real
    from backend.bets.models.bet import Bet


class Group(DataModel):
    """
    Group model.

    - members: usernames (List[str])
    - admin_username: username (str)
    - bets:
        * a BBDD: guardem UUID[] (ids de bet)
        * a API: podem hidratar bets com List[Bet] i retornar-les serialitzades
    """

    __id: GroupId
    __name: GroupName
    __create_date: GroupCreateDate
    __update_date: GroupUpdateDate

    __members: list[str]
    __admin_username: str

    __bet_ids: list[UUID]
    __bets: list["Bet"] | None

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        name: str,
        create_date: datetime,
        update_date: datetime,
        members: list[str],
        admin_username: str,
        bets: list[str | UUID] | None = None,          # ids (del camp groups.bets)
        hydrated_bets: list["Bet"] | None = None,      # opcional: bets completes
    ) -> None:
        self.__id = GroupId(value=id)
        self.__name = GroupName(value=name)
        self.__create_date = GroupCreateDate(value=create_date)
        self.__update_date = GroupUpdateDate(value=update_date)

        self.__members = members
        self.__admin_username = admin_username

        self.__bet_ids = [UUID(str(x)) for x in (bets or [])]
        self.__bets = hydrated_bets

    @property
    def id(self) -> str | UUID:
        return self.__id.value

    @property
    def name(self) -> str:
        return self.__name.value

    @property
    def create_date(self) -> datetime:
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        return self.__update_date.value

    @update_date.setter
    def update_date(self, value: datetime) -> None:
        self.__update_date = GroupUpdateDate(value=value)

    @property
    def members(self) -> list[str]:
        return self.__members

    @property
    def admin_username(self) -> str:
        return self.__admin_username

    # Alias (per si tens codi vell que fa servir admin_id)
    @property
    def admin_id(self) -> str:
        return self.__admin_username

    @property
    def bet_ids(self) -> list[UUID]:
        return self.__bet_ids

    @property
    def bets(self) -> list["Bet"]:
        return self.__bets or []

    def set_bets(self, bets: list["Bet"]) -> None:
        """Hidrata bets completes i sincronitza bet_ids."""
        self.__bets = bets
        self.__bet_ids = [UUID(str(b.id)) for b in bets]

    def to_persistence_dict(self) -> dict[str, Any]:
        """Dict per guardar a Postgres."""
        return {
            "id": self.id,
            "name": self.name,
            "create_date": self.create_date,
            "update_date": self.update_date,
            "members": self.members,                 # TEXT[]
            "admin_username": self.admin_username,   # TEXT
            "bets": self.bet_ids,                    # UUID[]
        }

    def to_dict(self) -> dict[str, Any]:
        """
        Dict per resposta API (schema GroupGetSchema).
        Si no estan hidratades, retorna bets = [].
        """
        bets_payload: list[Any] = []
        if self.__bets:
            # Suposo que Bet hereta DataModel i té to_dict()
            bets_payload = [b.to_dict() for b in self.__bets]

        return {
            "id": self.id,
            "name": self.name,
            "create_date": self.create_date,
            "update_date": self.update_date,
            "members": self.members,
            "admin_username": self.admin_username,
            "bets": bets_payload,
        }
