"""
UserRoleIdMother module.
"""

from backend.users.models import UserRoleId
from tests.shared.models.mothers import IdentifierMother


class UserRoleIdMother(IdentifierMother):
    """
    UserRoleIdMother class.
    """

    @classmethod
    def create(cls, value: str | None = None) -> UserRoleId:
        """
        Create a user role id. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User id value. Defaults to None.

        Returns:
            UserRoleId: User role id.
        """
        if value is None:
            value = cls.random()

        return UserRoleId(value=value)
