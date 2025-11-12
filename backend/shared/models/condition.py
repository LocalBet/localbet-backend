"""
SQL condition operations.
"""

from typing import Any, Generic, TypeVar
from typing_extensions import override

from pydantic import model_validator

from backend.shared.errors import ConditionError

from .data_model import DataModel
from .sql_operations import SQLOperation

T = TypeVar("T", bound=DataModel)


class Condition(Generic[T], DataModel):
    """
    SQL condition operations.
    """

    __field: str
    __operator: SQLOperation
    __value: str

    def __init__(self, field: str, operator: SQLOperation, value: Any) -> None:
        """
        Condition constructor.

        Args:
            field (str): Field to be compared.
            operator (SQLOperation): Operator to be used in the comparison.
            value (Any): Value to be compared with the field.
        """
        self.__field = field
        self.__operator = operator
        self.__value = value

    @override
    def __eq__(self, other: object) -> bool:
        """
        Equality comparison between two Condition objects.

        Args:
            other (object): The other object to compare with.

        Returns:
            bool: True if both Condition objects are equal, False otherwise.
        """
        if not isinstance(other, Condition):
            return NotImplemented

        return (
            self.field == other.field
            and self.operator == other.operator
            and self.value == other.value
        )

    @property
    def field(self) -> str:
        """
        Field to be compared.
        """
        return self.__field

    @property
    def operator(self) -> str:
        """
        Operator to be used in the comparison.
        """
        return self.__operator

    @property
    def value(self) -> str:
        """
        Value to be compared with the field.
        """
        return self.__value

    @model_validator(mode="before")
    @classmethod
    def validate_field(cls, values: dict[Any, Any]) -> dict[Any, Any]:
        """
        Validate that the field is a valid column of the data model.
        """
        field_name = values.get("field")
        model = cls.__annotations__.get("T")  # Get the generic model type

        if model and isinstance(field_name, str) and not hasattr(model, field_name):
            raise ConditionError(condition=cls(**values))

        return values
