"""
User domain model.
"""

from datetime import datetime
from typing_extensions import override
from uuid import UUID

from backend.shared.models import DataModel

from .user_create_date import UserCreatedDate
from .user_email import UserEmail
from .user_id import UserId
from .user_name import UserName
from .user_password import UserPassword
from .user_role_id import UserRoleId
from .user_update_date import UserUpdatedDate
from .user_username import UserUsername


class User(DataModel):
    """
    User model.
    """

    __id: UserId
    __name: UserName
    __username: UserUsername
    __email: UserEmail
    __role_id: UserRoleId
    __password: UserPassword
    __create_date: UserCreatedDate
    __update_date: UserUpdatedDate

    # It's necessary to redefine __hash__ because __eq__ is overridden
    __hash__ = DataModel.__hash__

    def __init__(
        self,
        id: str | UUID,
        name: str,
        username: str,
        email: str,
        password: str,
        role_id: str | UUID,
        create_date: datetime,
        update_date: datetime,
    ) -> None:
        """
        User domain model constructor.

        Args:
            id (str): User id.
            name (str): User name.
            username (str): User username.
            email (str): User email.
            password (str): User password.
            create_date (datetime): User created date.
            update_date (datetime): User updated date.
        """
        self.__id = UserId(value=id)
        self.__name = UserName(value=name)
        self.__username = UserUsername(value=username)
        self.__email = UserEmail(value=email)
        self.__password = UserPassword(value=password)
        self.__role_id = UserRoleId(value=role_id)
        self.__create_date = UserCreatedDate(value=create_date)
        self.__update_date = UserUpdatedDate(value=update_date)

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the user is equal to another user. This method is overridden to exclude the password field from the
        comparison because the password is hashed and salted every time it is saved, making it unique even for the same
        password.

        Args:
            other (object): The object to compare with this user.

        Returns:
            bool: True if the users are equal (excluding the password), False otherwise.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        self_dict = self.to_dict()
        self_dict.pop("password")

        other_dict = other.to_dict()
        other_dict.pop("password")

        return self_dict == other_dict

    @property
    def id(self) -> str | UUID:
        """
        Returns the user's id.

        Returns:
            str | UUID: User id.
        """
        return self.__id.value

    @property
    def name(self) -> str:
        """
        Returns the user's name as a primitive type.

        Returns:
            str: User name.
        """
        return self.__name.value

    @name.setter
    def name(self, value: str) -> None:
        """
        Sets the user's name.

        Args:
            value (str): User name.
        """
        self.__name = UserName(value=value)

    @property
    def username(self) -> str:
        """
        Returns the user's username as a primitive type.

        Returns:
            str: User username.
        """
        return self.__username.value

    @username.setter
    def username(self, value: str) -> None:
        """
        Sets the user's username.

        Args:
            value (str): User username.
        """
        self.__username = UserUsername(value=value)

    @property
    def email(self) -> str:
        """
        Returns the user's email as a primitive type.

        Returns:
            str: User email.
        """
        return self.__email.value

    @email.setter
    def email(self, value: str) -> None:
        """
        Sets the user's email.

        Args:
            value (str): User email.
        """
        self.__email = UserEmail(value=value)

    @property
    def password(self) -> str:
        """
        Returns the user's password as a primitive type.

        Returns:
            str: User password.
        """
        return self.__password.value

    @password.setter
    def password(self, value: str) -> None:
        """
        Sets the user's password.

        Args:
            value (str): User password.
        """
        self.__password = UserPassword(value=value)

    def check_password(self, plain_password: str) -> bool:
        """
        Checks if the provided password matches the user's password.

        Args:
            plain__password (str): Password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return self.__password == plain_password

    @property
    def role_id(self) -> str | UUID:
        """
        Returns the user's role id.

        Returns:
            str | UUID: User role id.
        """
        return self.__role_id.value

    @role_id.setter
    def role_id(self, value: str | UUID) -> None:
        """
        Sets the user's role id.

        Args:
            value (str | UUID): User role id.
        """
        self.__role_id = UserRoleId(value=value)

    @property
    def create_date(self) -> datetime:
        """
        Returns the user's created date as a primitive type.

        Returns:
            datetime: User created date.
        """
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        """
        Returns the user's updated date as a primitive type.

        Returns:
            datetime: User updated date.
        """
        return self.__update_date.value

    @update_date.setter
    def update_date(self, value: datetime) -> None:
        """
        Sets the user's updated date.

        Args:
            value (datetime): User updated date.
        """
        self.__update_date = UserUpdatedDate(value=value)
