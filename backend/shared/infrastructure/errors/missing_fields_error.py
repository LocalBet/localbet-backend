"""
MissingFieldsError module.
"""

from collections.abc import Iterable

from .infrastructure_base_error import InfrastructureBaseError


class MissingFieldsError(InfrastructureBaseError):
    """
    MissingFieldsError class.
    """

    __missing_fields: Iterable[str]

    def __init__(self, *, missing_fields: Iterable[str]) -> None:
        """
        MissingFieldsError constructor.

        Args:
            missing_fields (Iterable[str]): The missing fields.
        """
        self.__missing_fields = missing_fields

        message = f'Missing request arguments: {", ".join(missing_fields)}.'
        super().__init__(message=message)

    @property
    def missing_fields(self) -> Iterable[str]:
        """
        Returns the missing fields.

        Returns:
            Iterable[str]: The missing fields.
        """
        return self.__missing_fields
