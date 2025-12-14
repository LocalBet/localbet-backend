"""
UserCoins value object.
"""

from backend.shared.models import ValueObject


class UserCoins(ValueObject[int]):
    """
    User coins value object (discrete integer).
    """

    def _validate(self, value: int) -> None:
        try:
            v = int(value)
        except (TypeError, ValueError) as e:
            raise TypeError("UserCoins must be an integer") from e

        if v < 0:
            raise ValueError("UserCoins cannot be negative")
