"""
GroupRoleType domain model.
"""

from datetime import datetime
from uuid import UUID

from backend.shared.models import DataModel
from backend.group_roles_type.models import GroupRoleTypeId, GroupRoleTypeName, GroupRoleTypeDescription, GroupRoleTypeCreatedDate, GroupRoleTypeUpdateDate, G

class GroupRoleType(DataModel):
    """Simple GroupRoleType domain model."""

    __id: GroupRoleTypeId
    __group_id:
    __name: GroupRoleTypeName
    __description: GroupRoleTypeDescription
    __create_date: GroupRoleTypeCreatedDate
    __update_date: GroupRoleTypeUpdateDate

    def __init__(self, id: str | UUID, name: str, description: str | None, create_date: datetime | str, update_date: datetime | str) -> None:
        self.__id = GroupRoleTypeId(value=id)
        self.__name = GroupRoleTypeName(value=name)
        self.__description = GroupRoleTypeDescription(value=description)
        self.__create_date = GroupRoleTypeCreatedDate(value=create_date)
        self.__update_date = GroupRoleTypeUpdateDate(value=update_date)

    @property
    def id(self) -> str:
        return self.__id.value

    @property
    def name(self) -> str:
        return self.__name.value

    @name.setter
    def name(self, value: str) -> None:
        self.__name = GroupRoleTypeName(value=value)

    @property
    def create_date(self) -> datetime:
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        return self.__update_date.value

    @update_date.setter
    def update_date(self, value: datetime | str) -> None:
        self.__update_date = GroupRoleTypeUpdateDate(value=value)
