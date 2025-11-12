"""
UserNameMother module.
"""

from backend.users.models import UserName
from tests.shared.models.mothers import NameMother


class UserNameMother(NameMother):
    """
    UserNameMother class.
    """

    @classmethod
    def create(cls, value: str | None = None) -> UserName:
        """
        Create a user name. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User name value. Defaults to None.

        Returns:
            UserName: User name.
        """
        if value is None:
            value = cls.random()

        return UserName(value=value)
