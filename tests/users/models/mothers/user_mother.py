"""
UserMother module.
"""

from datetime import datetime

from backend.users.models import User

from .user_created_date_mother import UserCreatedDateMother
from .user_email_mother import UserEmailMother
from .user_id_mother import UserIdMother
from .user_name_mother import UserNameMother
from .user_password_mother import UserPasswordMother
from .user_role_id_mother import UserRoleIdMother
from .user_updated_date_mother import UserUpdatedDateMother
from .user_username_mother import UserUsernameMother


class UserMother:
    """
    UserMother class.
    """

    @classmethod
    def create(
        cls,
        id: str | None = None,
        name: str | None = None,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        role_id: str | None = None,
        created_date: datetime | None = None,
        updated_date: datetime | None = None,
    ) -> User:
        """
        Create a user.

        Args:
            id (str, optional): User id. Defaults to None.
            name (str, optional): User name. Defaults to None.
            username (str, optional): User username. Defaults to None.
            email (str, optional): User email. Defaults to None.
            password (str, optional): User password. Defaults to None.
            role_id (str, optional): User role id. Defaults to None.
            created_date (datetime, optional): User created date. Defaults to None.
            updated_date (datetime, optional): User updated date. Defaults to None.

        Returns:
            User: User.
        """
        return User(
            id=UserIdMother.create(value=id).value,
            name=UserNameMother.create(value=name).value,
            username=UserUsernameMother.create(value=username).value,
            email=UserEmailMother.create(value=email).value,
            role_id=UserRoleIdMother.create(value=role_id).value,
            password=UserPasswordMother.create(value=password).value,
            create_date=UserCreatedDateMother.create(value=created_date).value,
            update_date=UserUpdatedDateMother.create(value=updated_date).value,
        )
