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

    @classmethod
    def with_subdomain(cls) -> UserEmail:
        """
        Create a user email with a subdomain.

        Returns:
            UserEmail: User email with subdomain.
        """
        email = cls.random(domain="mail.example.com")
        return UserEmail(value=email)

    @classmethod
    def with_plus_sign(cls) -> UserEmail:
        """
        Create a user email with a plus sign.

        Returns:
            UserEmail: User email with plus sign.
        """
        local_part = cls._faker().user_name() + "+tag"
        domain = "example.com"
        email = f"{local_part}@{domain}"
        return UserEmail(value=email)

    @classmethod
    def with_dots_in_local_part(cls) -> UserEmail:
        """
        Create a user email with dots in the local part.

        Returns:
            UserEmail: User email with dots in local part.
        """
        local_part = "first.last"
        domain = "example.com"
        email = f"{local_part}@{domain}"
        return UserEmail(value=email)
