from backend.shared.models import ValueObject
from backend.bets.errors.errors import BetStatusError

class BetStatus(ValueObject[str]):
    __VALID_STATUSES = {"pending", "won", "lost"}

    def _validate(self, value: str) -> None:
        if value not in self.__VALID_STATUSES:
            raise BetStatusError(status=value)
