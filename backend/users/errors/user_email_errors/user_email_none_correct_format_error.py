"""
UserEmailNoneCorrectFormatError module.
"""

from backend.shared.errors import ValidationError


class UserEmailNoneCorrectFormatError(ValidationError):
    """
    UserEmailNoneCorrectFormatError class.
    """

    def __init__(self) -> None:
        """
        UserEmailNoneCorrectFormatError constructor.
        """
        message = "UserEmail value has none correct format."
        super().__init__(message=message)
