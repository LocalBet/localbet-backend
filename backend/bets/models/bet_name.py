from backend.shared.models import ValueObject
from backend.bets.errors.errors import BetNameError

class BetName(ValueObject[str]):
    def _validate(self, value: str) -> None:
        if not value or len(value) < 3:
            raise BetNameError(name=value)
