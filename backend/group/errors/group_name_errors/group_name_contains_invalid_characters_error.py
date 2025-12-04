"""
GroupNameContainsInvalidCharactersError module.
"""

from backend.shared.errors import ValidationError


class GroupNameContainsInvalidCharactersError(ValidationError):
    """
    GroupNameContainsInvalidCharactersError class.
    """

    __name: str

    def __init__(self, *, name: str) -> None:
        """
        RoleNameContainsInvalidCharactersError constructor.

        Args:
            name (str): The value that caused the error.
        """
        self.__name = name

        message = f"GroupName value <<<{name}>>> contains invalid characters. Only printable characters are allowed."
        super().__init__(message=message)

    @property
    def name(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__name
