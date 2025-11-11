"""
IdentifierError module.
"""

from typing import Any


class ConditionError(Exception):
    """
    IdentifierError class.
    """

    __condition: Any

    def __init__(self, condition: Any) -> None:
        """
        ConditionError constructor.

        Args:
            condition (Any): The value that caused the error.
        """
        self.__condition = condition

        message = f"Condition value <<<{condition}>>> must be a valid condition."
        super().__init__(message)

    @property
    def condition(self) -> Any:
        """
        Returns the value that caused the error.

        Returns:
            Any: The value that caused the error.
        """
        return self.__condition
