"""
UserPasswordMinLengthError module.
"""

from backend.shared.errors import ValidationError


class UserPasswordMinLengthError(ValidationError):
    """
    UserPasswordMinLengthError class.
    """

    __min_length: int

    def __init__(self, *, min_length: int) -> None:
        """
        UserPasswordMinLengthError constructor.

        Args:
            min_length (int): The minimum allowed length.
        """
        self.__min_length = min_length

        message = f"UserPassword value must be at least <<<{min_length}>>> characters long."
        super().__init__(message=message)

    @property
    def min_length(self) -> int:
        """
        Returns the minimum allowed length.

        Returns:
            int: The minimum allowed length.
        """
        return self.__min_length
