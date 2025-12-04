"""
GroupRoleTypeDescriptionMaxLengthError module.
"""

from backend.shared.errors import ValidationError


class GroupRoleTypeDescriptionMaxLengthError(ValidationError):
    """
    GroupRoleTypeDescriptionMaxLengthError class.
    """

    __name: str
    __max_length: int

    def __init__(self, *, name: str, max_length: int) -> None:
        """
        GroupRoleTypeDescriptionMaxLengthError constructor.

        Args:
            name (str): The value that caused the error.
            max_length (int): The maximum allowed length.
        """
        self.__name = name
        self.__max_length = max_length

        message = f'GroupRoleTypeDescription value <<<{name}>>> must be at most <<<{max_length}>>> characters long. Got <<<{len(name)}>>> characters.'  # noqa: E501 # fmt: skip
        super().__init__(message=message)

    @property
    def name(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__name

    @property
    def max_length(self) -> int:
        """
        Returns the maximum allowed length.

        Returns:
            int: The maximum allowed length.
        """
        return self.__max_length
