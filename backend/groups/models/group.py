"""
Group domain model.
"""

from datetime import datetime
from typing_extensions import override
from uuid import UUID

from backend.shared.models import DataModel

from .group_id import GroupId
from .group_name import GroupName
from .group_create_date import GroupCreateDate
from .group_update_date import GroupUpdateDate
from .group_user_id import GroupUserId
from .group_admin_id import GroupAdminId


class Group(DataModel):
    """
    Group model.
    """

    __id: GroupId
    __name: GroupName
    __create_date: GroupCreateDate
    __update_date: GroupUpdateDate
    __members: list[GroupUserId]
    __admin_id: GroupAdminId

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        name: str,
        create_date: datetime,
        update_date: datetime,
        members: list[GroupUserId],
        admin_id: str | UUID,
    ) -> None:
        """
        Group domain model constructor.

        Args:
            id (str): Group id.
            name (str): Group name.
            create_date (datetime): Group created date.
            update_date (datetime): Group update date.
            members (list): List of members in the group.
            admin_id (str | UUID): ID of the group admin.
        """
        self.__id = GroupId(value=id)
        self.__name = GroupName(value=name)
        self.__create_date = GroupCreateDate(value=create_date)
        self.__update_date = GroupUpdateDate(value=update_date)
        self.__members = members
        self.__admin_id = GroupAdminId(value=admin_id)

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

    @property
    def members(self) -> list[GroupUserId]:
        return self.__members

    @property
    def admin_id(self) -> str | UUID:
        return self.__admin_id.value
