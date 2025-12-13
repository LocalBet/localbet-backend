"""
BetCost value object.
"""

from backend.shared.models import ValueObject


class BetCost(ValueObject[float]):
    """
    Cost (entry fee) in coins to join the bet.
    """

    def _validate(self, value: float) -> None:
        try:
            v = float(value)
        except (TypeError, ValueError) as e:
            raise TypeError("BetCost must be a number") from e

        if v < 0:
            raise ValueError("BetCost cannot be negative")
