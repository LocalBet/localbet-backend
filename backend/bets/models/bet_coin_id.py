"""
BetCoinId value object.
"""

from backend.shared.models import ID
from backend.bets.errors.errors import BetCoinIdError


class BetCoinId(ID):
    """
    BetCoinId value object.
    """

    def _validate(self, value: str) -> None:
        try:
            super()._validate(value)
        except Exception:
            raise BetCoinIdError(coin_id=value)
