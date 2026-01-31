"""
Update GroupRoleType service.
"""

from backend.group_roles_type.models import GroupRoleType
from uuid import UUID
from datetime import datetime, UTC
from backend.group_roles_type.actions import GroupRoleTypeActions

class GroupRoleTypeUpdateService:
    """
    Update GroupRoleType service.
    """

    __action: GroupRoleTypeActions

    def __init__(self, action: GroupRoleTypeActions):
        """
        GroupRoleType update service constructor.

        Args:
            action (GroupRoleTypeActions): GroupRoleType action.
        """
        self.__action = action

    def update(self,
               group_role_type: GroupRoleType,
               name: str | None,
               description: str | None,
               ) -> None:
        """
        Update GroupRoleType.
        The parameters with the same value or None will not be updated.

        Args:
            group_role_type (GroupRoleType): GroupRoleType to update.
            name (str | None): New name.
            description (str | None): New description.

        Raises:
            GroupRoleTypeNotFoundError: If GroupRoleType is not found.
        """
        if name is not None:
            group_role_type.name = name

        if description is not None:
            group_role_type.description = description

        group_role_type.update_date = datetime.now(UTC)
        self.__action.update(group_role_type=group_role_type)