"""
Permission actions interface.
"""

from abc import ABC, abstractmethod

from backend.shared.models import Condition, DataModel
from backend.permissions.models import Permission


class PermissionActions(ABC):
    """
    Abstract class for permission action. To define user able actions.
    """

    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[Permission]:
        """
        Search a permission in the action by conditions.

        Args:
        conditions (list[Condition]): Conditions to search for.

        Returns:
        list[Permission]: List of permissions.
        """
        ...
