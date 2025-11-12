"""
NoRowAffectedError module.
"""

from psycopg import IntegrityError


class NoRowAffectedError(IntegrityError):
    """
    NoRowAffectedError class.
    """

    def __init__(self) -> None:
        """
        NoRowAffectedError constructor.
        """
        message = "The executed query did not affect any rows."
        super().__init__(message)
