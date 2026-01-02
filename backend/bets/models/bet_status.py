from backend.shared.models import ValueObject
from backend.bets.errors.errors import BetStatusError

class BetStatus(ValueObject[str]):
    """
    Bet status value object.
    
    Valid statuses per SQL schema (04_tables.sql line 124):
    - 'active': open for participation
    - 'closed': deadline passed
    - 'resolved': winner determined
    """
    __VALID_STATUSES = {"active", "closed", "resolved"}

    def _validate(self, value: str) -> None:
        if value not in self.__VALID_STATUSES:
            raise BetStatusError(status=value)
