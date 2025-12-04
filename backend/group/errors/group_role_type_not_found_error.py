"""
GroupRoleTypeNotFoundError module.
"""

from typing import Any

from backend.shared.errors import DomainBaseError


class GroupRoleTypeNotFoundError(DomainBaseError):
    """
    GroupRoleTypeNotFoundError class.
    """

    __field: str
    __value: Any

    def __init__(self, *, field: str, value: Any) -> None:
        """
        GroupRoleTypeNotFoundError constructor.

        Args:
            field (str): The name of the field that caused the conflict.
            value (Any): The value of the field that caused the conflict, it must be stringifyable.
        """
        self.__field = field
        self.__value = value

        message = f"GroupRoleType with <<<{field}>>> <<<{value}>>> was not found."
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
