"""
UserCreatedDateMother module.
"""

from datetime import datetime

from backend.users.models import UserCreatedDate
from tests.shared.models.mothers import DatetimeMother


class UserCreatedDateMother(DatetimeMother):
    """
    UserCreatedDateMother class.
    """

    @classmethod
    def create(cls, value: datetime | None = None) -> UserCreatedDate:
        """
        Create an user created date. If the value is not provided, it will be randomly generated.

        Args:
            value (datetime, optional): User created date value. Defaults to None.

        Returns:
            UserCreatedDate: User created date.
        """
        if value is None:
            value = cls.random()

        return UserCreatedDate(value=value)
