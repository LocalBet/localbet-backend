"""
NoRowAffectedError module.
"""

from psycopg import IntegrityError

from .infrastructure_base_error import InfrastructureBaseError


class NoRowAffectedError(InfrastructureBaseError, IntegrityError):
    """
    NoRowAffectedError class.
    """

    def __init__(self) -> None:
        """
        NoRowAffectedError constructor.
        """
        message = "The executed query did not affect any rows."
        super().__init__(message=message)
