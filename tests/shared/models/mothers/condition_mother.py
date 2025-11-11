"""
ConditionMother to create Condition objects for tests.
"""

from secrets import choice

from backend.shared.models import Condition, DataModel, SQLOperation

from .word_mother import WordMother


class ConditionMother:
    """
    ConditionMother class to create Condition objects for tests.
    """

    @classmethod
    def create(
        cls,
        field: str | None = None,
        operator: SQLOperation | None = None,
        value: str | None = None,
    ) -> Condition[DataModel]:
        """Create a Condition with sensible defaults.

        Args:
            field (str, optional): Field to be compared. Defaults to a random word.
            operator (SQLOperation, optional): Operator to be used in the comparison. Defaults to a random SQLOperation.
            value (str, optional): Value to be compared with the field. Defaults to a random word.
        """
        if field is None:
            field = WordMother.random()

        if operator is None:
            operator = choice(seq=list(SQLOperation))

        if value is None:
            value = WordMother.random()

        return Condition(field=field, operator=operator, value=value)
