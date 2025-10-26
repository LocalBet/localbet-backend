"""
IDError module.
"""

from typing import Any

from .validation_error import ValidationError


class IDError(ValidationError):
    """
    IDError class.
    """

    __id: Any

    def __init__(self, id: Any) -> None:
        """
        IDError constructor.

        Args:
            id (Any): The value that caused the error.
        """
        self.__id = id

        message = f"id value <<<{id}>>> must be a valid UUID string."
        super().__init__(message=message)

    @property
    def id(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__id
