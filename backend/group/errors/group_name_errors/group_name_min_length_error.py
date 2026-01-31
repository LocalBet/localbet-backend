"""
GroupNameMinLengthError module.
"""

from backend.shared.errors import ValidationError


class GroupNameMinLengthError(ValidationError):
    """
    GroupNameMinLengthError class.
    """

    __name: str
    __min_length: int

    def __init__(self, *, name: str, min_length: int) -> None:
        """
        GroupNameMinLengthError constructor.

        Args:
            name (str): The value that caused the error.
            min_length (int): The minimum allowed length.
        """
        self.__name = name
        self.__min_length = min_length

        message = f'GroupName value <<<{name}>>> must be at least <<<{min_length}>>> characters long. Got <<<{len(name)}>>> characters.'  # noqa: E501 # fmt: skip
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
    def min_length(self) -> int:
        """
        Returns the minimum allowed length.

        Returns:
            int: The minimum allowed length.
        """
        return self.__min_length
