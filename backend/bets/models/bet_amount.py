from backend.shared.models import ValueObject
from backend.bets.errors.errors import BetAmountError

class BetAmount(ValueObject[float]):
    def _validate(self, value: float) -> None:
        if value <= 0:
            raise BetAmountError(amount=value)
