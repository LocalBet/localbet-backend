"""
UserCoins value object.
"""

from backend.shared.models import ValueObject


class UserCoins(ValueObject[float]):
    """
    User coins value object.
    """

    def _validate(self, value: float) -> None:
        try:
            v = float(value)
        except (TypeError, ValueError) as e:
            raise TypeError("UserCoins must be a number") from e

        if v < 0:
            raise ValueError("UserCoins cannot be negative")
