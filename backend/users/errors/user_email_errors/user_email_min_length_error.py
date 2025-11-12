"""
UserEmailMinLengthError module.
"""

from backend.shared.errors import ValidationError


class UserEmailMinLengthError(ValidationError):
    """
    UserEmailMinLengthError class.
    """

    __email: str
    __min_length: int

    def __init__(self, *, email: str, min_length: int) -> None:
        """
        UserEmailMinLengthError constructor.

        Args:
            email (str): The value that caused the error.
            min_length (int): The minimum allowed length.
        """
        self.__email = email
        self.__min_length = min_length

        message = f'UserEmail value <<<{email}>>> must be at least <<<{min_length}>>> characters long. Got <<<{len(email)}>>> characters.'  # noqa: E501 # fmt: skip
        super().__init__(message=message)

    @property
    def email(self) -> str:
        """
        Returns the value that caused the error.

        Returns:
            str: The value that caused the error.
        """
        return self.__email

    @property
    def min_length(self) -> int:
        """
        Returns the minimum allowed length.

        Returns:
            int: The minimum allowed length.
        """
        return self.__min_length
