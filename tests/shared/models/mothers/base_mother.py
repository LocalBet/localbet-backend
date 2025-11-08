"""
BaseMother module.
"""

from datetime import date, datetime
from random import choice
from typing import Any

from faker import Faker


class BaseMother:
    """
    BaseMother class.
    """

    __LOCALES = ('en_US', 'en_CA', 'en_GB', 'es_ES', 'pt_PT', 'fr_FR', 'it_IT')

    @classmethod
    def _faker(cls) -> Faker:
        """
        Get the Faker library object.

        Returns:
            Faker: Faker library object.
        """
        return Faker(locale=cls.__LOCALES)

    @classmethod
    def _invalid_type(cls, remove_types: set[type[Any]] | None = None) -> Any:  # noqa: C901
        """
        Create an invalid type.

        Args:
            remove_types (set[type[Any]], optional): Set of types to remove from the generated type. Defaults to None.

        Returns:
            Any: Invalid type.
        """
        faker = Faker(locale=cls.__LOCALES)

        if remove_types is None:
            remove_types = set()

        types: list[Any] = []
        if int not in remove_types:
            types.append(faker.pyint())

        if float not in remove_types:
            types.append(faker.pyfloat())

        if bool not in remove_types:
            types.append(faker.pybool())

        if str not in remove_types:
            types.append(faker.pystr())

        if bytes not in remove_types:
            types.append(faker.pystr().encode())

        if list not in remove_types:
            types.append(faker.pylist()) # type: ignore

        if set not in remove_types:
            types.append(faker.pyset()) # type: ignore

        if tuple not in remove_types:
            types.append(faker.pytuple()) # type: ignore

        if dict not in remove_types:
            types.append(faker.pydict()) # type: ignore

        if type(None) not in remove_types:
            types.append(None)

        if datetime not in remove_types:
            types.append(faker.date_time())

        if date not in remove_types:
            types.append(date.fromisoformat(faker.date()))

        return choice(seq=types)  # noqa: S311  # nosec
