"""
Base model module.
"""

from datetime import date, datetime
from typing import Any, Self

from typing_extensions import override


class DataModel:
    """
    Base data model class.
    """

    @override
    def __repr__(self) -> str:
        """
        Returns the class representation as a string.

        Returns:
            str: String representation of the class.
        """
        attributes: list[str] = []
        for key, value in self.to_dict().items():
            attributes.append(f"{key}={value}")

        return f"{self.__class__.__name__}({', '.join(attributes)})"

    @override
    def __hash__(self) -> int:
        """
        Returns the hash of the class.

        Returns:
            int: Hash of the class.
        """
        return hash(tuple(sorted(self.to_dict().items())))

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the class is equal to another object.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if the objects are equal, otherwise False.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.to_dict() == other.to_dict()

    @classmethod
    def from_dict(cls, primitives: dict[str, Any]) -> Self:
        """
        Create an instance of the class with a dictionary of its primitives.

        Args:
            primitives (dict[str, Any]): Dictionary to create the instance from.

        Returns:
            Self: Instance of the class.
        """
        return cls(**primitives)

    def to_dict(self) -> dict[str, Any]:
        """
        Returns the class as a dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the class.
        """
        dictionary: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            key = key.replace(f"_{self.__class__.__name__}__", "")

            if key.startswith("_"):
                key = key[1:]

            value = value.value if hasattr(value, "value") else value
            if isinstance(value, date | datetime):
                value = value.isoformat()

            dictionary[key] = value

        return dictionary
