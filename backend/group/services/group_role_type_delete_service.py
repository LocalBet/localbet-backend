"""
Delete GroupRoleType service.
"""

from backend.group_roles_type.errors import GroupRoleTypeNotFoundError
from backend.group_roles_type.actions import GroupRoleTypeActions
from backend.group_roles_type.models import GroupRoleType

class GroupRoleTypeDeleteService:
    """
    Delete GroupRoleType domain service.
    """

    __action: GroupRoleTypeActions

    def __init__(self, action: GroupRoleTypeActions) -> None:
        """
        GroupRoleType constructor.
        """
        self.__action = action


    def delete(self, group_role_type: GroupRoleType) -> None:
        """
        Delete a GroupRoleType

        Args:
            group_role_type (GroupRoleType): GroupRoleType to delete.

        Raises:
            GroupRoleTypeNotFoundError: If the GroupRoleType was not found.
        """
        self._ensure_none_exist_user_with_selected_role(group_role_type=group_role_type)
        self.__action.delete(group_role_type=group_role_type)

    def _ensure_none_exist_user_with_selected_role(self, group_role_type: GroupRoleType) -> None:
        """
        Ensure that none exist user inside the group with selected role to delete it.

        Args:
            group_role_type (GroupRoleType): Selected group role type to delete.
        """
        # TODO:
        pass

    def _ensure_group_role_type_exist(self, group_role_type: GroupRoleType) -> None:
        """
        Ensure that the selected group role type exist.

        Args:
            group_role_type (GroupRoleType): Selected group role type to delete.
        """
        # TODO:
        pass