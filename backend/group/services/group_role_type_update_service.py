"""
Update GroupRoleType service.
"""

from backend.group_roles_type.models import GroupRoleType
from backend.group_roles_type.errors import GroupRoleTypeNotFoundError
from uuid import UUID

class GroupRoleTypeUpdateService:
    """
    Update GroupRoleType service.
    """

    __action: GroupRoleType

    def __init__(self, action: GroupRoleType):
        """
        GroupRoleType update service constructor.

        Args:
            action (GroupRoleType): GroupRoleType action.
        """
        self.__action = action

    def update(self,
               group_role_type: GroupRoleType,
               group_id: str | UUID | None,
               name: str | None,
               description: str | None,
               ) -> None:
        """
        Update GroupRoleType.
        The parameters with the same value or None will not be updated.

        Args:
            group_role_type (GroupRoleType): GroupRoleType to update.
            group_id (str | UUID | None): New group_id.
            name (str | None): New name.
            description (str | None): New description.

        Raises:
            GroupRoleTypeNotFoundError: If GroupRoleType is not found.
        """
        if group_id is not None:
            group_role_type.