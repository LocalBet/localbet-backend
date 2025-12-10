"""
BetUserId value object.
"""

from backend.shared.models import ID
from backend.bets.errors.errors import BetUserIdError


class BetUserId(ID):
    """
    BetUserId value object.
    """

    def _validate(self, value: str) -> None:
        try:
            super()._validate(value)
        except Exception:
            raise BetUserIdError(user_id=value)
