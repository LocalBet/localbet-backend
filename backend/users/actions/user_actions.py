"""
User actions interface.
"""

from abc import ABC, abstractmethod

from backend.shared.models import Condition, DataModel
from backend.users.models import User


class UserActions(ABC):
    """
    Abstract class for user action. To define user able actions.
    """

    @abstractmethod
    def search(self, conditions: list[Condition[DataModel]]) -> list[User]:
        """
        Search a user in the action by conditions.

        Args:
            conditions (list[Condition]): Conditions to search for.

        Returns:
            list[User]: List of users.
        """
        ...

    @abstractmethod
    def update(self, user: User) -> None:
        """
        Update values in the action.

        Args:
            user (User): User to be updated.

        Raises:
            UserNotFoundError: If User is not found.
        """
        ...

    @abstractmethod
    def save(self, user: User) -> None:
        """
        Create a service in the action.

        Args:
            user (User): User to be created.

        Raises:
            UserAlreadyExistsError: If service already exists.
            UserNotFoundError: If service is not found.
        """
        ...

    @abstractmethod
    def delete(self, user: User) -> None:
        """
        Delete service from the action.

        Args:
            user (User): User to delete.

        Raises:
            UserNotFoundError: If user is not found.
        """
        ...
