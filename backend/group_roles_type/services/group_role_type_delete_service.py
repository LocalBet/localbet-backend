"""
Delete GroupRoleType service.
"""

from backend.group_roles_type.actions import GroupRoleTypeActions
from backend.group_roles_type.models import GroupRoleType
from .group_role_finder_service import GroupRoleTypeFinderService
from uuid import UUID
from backend.shared.models import Condition, SQLOperation

class GroupRoleTypeDeleteService:
    """
    Delete GroupRoleType domain service.
    """

    __finder: GroupRoleTypeFinderService
    __action: GroupRoleTypeActions

    def __init__(self, action: GroupRoleTypeActions, finder: GroupRoleTypeFinderService) -> None:
        """
        GroupRoleType constructor.
        """
        self.__action = action
        self.__finder = finder

    def delete(self, group_role_type: GroupRoleType) -> None:
        """
        Delete a GroupRoleType

        Args:
            group_role_type (GroupRoleType): GroupRoleType to delete.

        Raises:
            GroupRoleTypeNotFoundError: If the GroupRoleType was not found.
        """
        self.__action.delete(group_role_type=group_role_type)

    def _ensure_group_role_type_exist(self, group_role_type_id: str | UUID) -> None:
        """
        Ensure that the selected group role type exist.

        Args:
            group_role_type_id (str | UUID): Selected group role type ID to delete.
        """
        self.__finder.find(
            conditions=[Condition(field='id', operator=SQLOperation.EQUAL, value=group_role_type_id)]
        )