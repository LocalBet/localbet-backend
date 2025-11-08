"""
UserUsernameMother module.
"""

from backend.users.models import UserUsername
from tests.shared.models.mothers import UsernameMother


class UserUsernameMother(UsernameMother):
    """
    UserUsernameMother class.
    """

    @classmethod
    def create(cls, value: str | None = None) -> UserUsername:
        """
        Create a user username. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User username value. Defaults to None.

        Returns:
            UserUsername: User username.
        """
        if value is None:
            value = cls.random()

        return UserUsername(value=value)
