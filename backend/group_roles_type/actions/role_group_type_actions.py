"""
RoleGroupType actions interface / scaffold.
"""

from abc import ABC, abstractmethod

from backend.group_roles_type.models import GroupRoleType
from backend.shared.models import Condition, DataModel


class GroupRoleTypeActions(ABC):
    """
    Abstract class for GroupRoleType action. To define RoleGroupType able actions.
    """

    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[GroupRoleType]:
        """
        Search a RoleGroup in the action by conditions.

        Args:
            conditions (list[Condition[DataModel]]): Conditions to search for.

        Returns:
            list[GroupRoleType]: List of RoleGroups.
        """
        ...

    @abstractmethod
    def update(self, group_role_type: GroupRoleType) -> None:
        """
        Update values in the action.

        Args:
            group_role_type (GroupRoleType): GroupRoleType to be updated.

        Raises:
            RoleGroupNotFoundError: If RoleGroup is not found.
        """
        ...

    @abstractmethod
    def save(self, group_role_type: GroupRoleType) -> None:
        """
        Create a RoleGroup in the action.

        Args:
        group_role_type (GroupRoleType): GroupRoleType to be created.

        Raises:
            RoleGroupAlreadyExistsError: If RoleGroup already exists.
            RoleGroupNotFoundError: If RoleGroup is not found.
        """
        ...

    @abstractmethod
    def delete(self, group_role_type: GroupRoleType) -> None:
        """
        Delete RoleGroup from the action.

        Args:
            group_role_type (GroupRoleType): RoleGroup to be deleted.

        Raises:
            RoleGroupNotFoundError: If RoleGroup is not found.
        """
        ...
