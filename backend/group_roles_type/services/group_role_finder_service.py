"""
GroupRoleType service scaffold.
"""

from datetime import datetime

from backend.shared.models import Condition, DataModel
from backend.group_roles_type.actions import GroupRoleTypeActions
from backend.group_roles_type.models import GroupRoleType
from backend.group_roles_type.errors import GroupRoleTypeNotFoundError

class GroupRoleTypeFinderService:
    """
    Find a user domain service.
    """

    __action: GroupRoleTypeActions

    def __init__(self, action: GroupRoleTypeActions) -> None:
        """
        GroupRoleTypeFinder constructor.
        """
        self.__action = action

    def find(self, conditions: list[Condition[DataModel]]) -> list[GroupRoleType]:
        """
        Find a GroupRoleType.

        Args:
            conditions (list[Condition]): Conditions to find the GroupRoleType.

        Raises:
            list[GroupRoleType]: Found GroupRoleType.
        """
        group_role_types = self.__action.search(conditions=conditions)

        if not group_role_types:
            raise GroupRoleTypeNotFoundError(field="conditions", value=conditions)

        return group_role_types