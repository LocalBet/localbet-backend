"""
UserUpdatedDateMother module.
"""

from datetime import datetime

from backend.users.models import UserUpdatedDate
from tests.shared.models.mothers import DatetimeMother


class UserUpdatedDateMother(DatetimeMother):
    """
    UserUpdatedDateMother class.
    """

    @classmethod
    def create(cls, value: datetime | None = None) -> UserUpdatedDate:
        """
        Create an user updated date. If the value is not provided, it will be randomly generated.

        Args:
            value (datetime, optional): User updated date value. Defaults to None.

        Returns:
            UserUpdatedDate: User updated date.
        """
        if value is None:
            value = cls.random()

        return UserUpdatedDate(value=value)
