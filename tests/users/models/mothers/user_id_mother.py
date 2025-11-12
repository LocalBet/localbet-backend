"""
UserIdMother module.
"""

from backend.users.models import UserId
from tests.shared.models.mothers import IdentifierMother


class UserIdMother(IdentifierMother):
    """
    UserIdMother class.
    """

    @classmethod
    def create(cls, value: str | None = None) -> UserId:
        """
        Create a user id. If the value is not provided, it will be randomly generated.

        Args:
            value (str, optional): User id value. Defaults to None.

        Returns:
            UserId: User id.
        """
        if value is None:
            value = cls.random()

        return UserId(value=value)
