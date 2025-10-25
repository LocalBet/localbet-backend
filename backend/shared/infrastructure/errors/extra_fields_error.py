"""
ExtraFieldsError module.
"""

from collections.abc import Iterable

from .infrastructure_base_error import InfrastructureBaseError


class ExtraFieldsError(InfrastructureBaseError):
    """
    ExtraFieldsError class.
    """

    __extra_fields: Iterable[str]

    def __init__(self, *, extra_fields: Iterable[str]) -> None:
        """
        ExtraFieldsError constructor.

        Args:
            extra_fields (Iterable[str]): The extra fields.
        """
        self.__extra_fields = extra_fields

        message = f'Unrecognized request arguments supplied: {", ".join(extra_fields)}.'
        super().__init__(message=message)

    @property
    def extra_fields(self) -> Iterable[str]:
        """
        Returns the extra fields.

        Returns:
            Iterable[str]: The extra fields.
        """
        return self.__extra_fields
