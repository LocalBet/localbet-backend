"""
User domain model.
"""

from datetime import datetime
from uuid import UUID

from typing_extensions import override

from backend.shared.models import DataModel
from backend.users.models import (
    UserCreatedDate,
    UserEmail,
    UserId,
    UserName,
    UserPassword,
    UserUpdatedDate,
    UserUsername,
)


class User(DataModel):
    """
    User model.
    """

    __id: UserId
    __name: UserName
    __username: UserUsername
    __email: UserEmail
    __password: UserPassword
    __created_date: UserCreatedDate
    __updated_date: UserUpdatedDate

    def __init__(
        self,
        id: str | UUID,
        name: str,
        username: str,
        email: str,
        password: str,
        created_date: datetime,
        updated_date: datetime,
    ) -> None:
        """
        User domain model constructor.

        Args:
            id (str): User id.
            name (str): User name.
            username (str): User username.
            email (str): User email.
            password (str): User password.
            created_date (datetime): User created date.
            updated_date (datetime): User updated date.
        """
        self.__id = UserId(value=id)
        self.__name = UserName(value=name)
        self.__username = UserUsername(value=username)
        self.__email = UserEmail(value=email)
        self.__password = UserPassword(value=password)
        self.__created_date = UserCreatedDate(value=created_date)
        self.__updated_date = UserUpdatedDate(value=updated_date)

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
    def created_date(self) -> datetime:
        """
        Returns the user's created date as a primitive type.

        Returns:
            datetime: User created date.
        """
        return self.__created_date.value

    @property
    def updated_date(self) -> datetime:
        """
        Returns the user's updated date as a primitive type.

        Returns:
            datetime: User updated date.
        """
        return self.__updated_date.value

    @updated_date.setter
    def updated_date(self, value: datetime) -> None:
        """
        Sets the user's updated date.

        Args:
            value (datetime): User updated date.
        """
        self.__updated_date = UserUpdatedDate(value=value)
