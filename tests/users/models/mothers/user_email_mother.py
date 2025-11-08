"""
UserEmailMother module.
"""

from backend.users.models import UserEmail
from tests.shared.models.mothers import EmailMother


class UserEmailMother(EmailMother):
    """
    UserEmailMother class.
    """

    @classmethod
    def create(cls, value: str | None = None, domain: str | None = None) -> UserEmail:
        """
        Create a user email. If the value is not provided, it will be randomly generated.

        Args:
            value (str): User email.
            domain (str, optional): Email domain. Defaults to None.

        Returns:
            UserEmail: User email.
        """
        if value is None:
            value = cls.random(domain=domain)

        return UserEmail(value=value)
