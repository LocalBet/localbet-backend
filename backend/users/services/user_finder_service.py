"""
Find a user domain service.
"""

from backend.shared.models import Condition, DataModel
from backend.users.actions import UserActions
from backend.users.errors import UserNotFoundError
from backend.users.models import User


class UserFinderService:
    """
    Find a user domain service.
    """

    __action: UserActions

    def __init__(self, action: UserActions) -> None:
        self.__action = action

    def find(self, conditions: list[Condition[DataModel]]) -> list[User]:
        """
        Find a user.

        Raises:
            UserNotFoundError: If user is not found.
        """
        users = self.__action.search(conditions=conditions)

        if not users:
            raise UserNotFoundError(field="conditions", value=conditions)

        return users
