"""
UserNotFoundError module.
"""

from typing import Any

from backend.shared.errors import DomainBaseError


class UserNotFoundError(DomainBaseError):
    """
    UserNotFoundError class.
    """

    __field: str
    __value: Any

    def __init__(self, *, field: str, value: Any) -> None:
        """
        UserNotFoundError constructor.

        Args:
            field (str): The name of the field that caused the conflict (e.g., 'username' or 'email').
            value (Any): The value of the field that caused the conflict, it must be stringifyable.
        """
        self.__field = field
        self.__value = value

        message = f'User with <<<{field}>>> <<<{value}>>> was not found.'
        super().__init__(message=message)

    @property
    def field(self) -> str:
        """
        Returns the field name that caused the conflict.

        Returns:
            str: The field name.
        """
        return self.__field

    @property
    def value(self) -> Any:
        """
        Returns the field value that caused the conflict.

        Returns:
            Any: The field value.
        """
        return self.__value
