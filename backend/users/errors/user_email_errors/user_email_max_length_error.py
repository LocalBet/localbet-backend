"""
UserEmailMaxLengthError module.
"""

from backend.shared.errors import ValidationError


class UserEmailMaxLengthError(ValidationError):
    """
    UserEmailMaxLengthError class.
    """

    __max_length: int

    def __init__(self, *, max_length: int) -> None:
        """
        UserEmailMaxLengthError constructor.

        Args:
            max_length (int): The maximum allowed length.
        """
        self.__max_length = max_length

        message = f"UserEmail value must be at most <<<{max_length}>>> characters long."
        super().__init__(message=message)

    @property
    def max_length(self) -> int:
        """
        Returns the maximum allowed length.

        Returns:
            int: The maximum allowed length.
        """
        return self.__max_length
