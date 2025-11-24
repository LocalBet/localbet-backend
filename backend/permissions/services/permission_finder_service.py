"""
Find a permission domain service.
"""

from backend.permissions.actions import PermissionActions
from backend.permissions.errors import PermissionNotFoundError
from backend.permissions.models import Permission
from backend.shared.models import Condition, DataModel


class PermissionFinderService:
    """
    Find a permission domain service.
    """

    __action: PermissionActions

    def __init__(self, action: PermissionActions) -> None:
        """
        PermissionFinderService constructor.
        """
        self.__action = action

    def find(self, conditions: list[Condition[DataModel]]) -> list[Permission]:
        """
        Find a permission.

        Args:
            conditions (list[Condition]): Conditions to find the permission.

        Raises:
            PermissionNotFoundError: If permission is not found.

        Returns:
        list[Permission]: List of found permission.
        """
        users = self.__action.search(conditions=conditions)

        if not users:
            raise PermissionNotFoundError(field="conditions", value=conditions)

        return users
