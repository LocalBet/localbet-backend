"""
Bet-related error classes.
"""

from backend.shared.infrastructure.errors import HTTPError


class BetNotFoundError(HTTPError):
    """
    Raised when a bet is not found.
    """

    def __init__(self, field: str, value: object) -> None:
        super().__init__(
            status_code=404,
            title="Bet Not Found",
            message=f"Bet with {field}={value} was not found.",
        )


class BetIdTypeError(HTTPError):
    """
    Raised when the bet ID is not a valid UUID.
    """

    def __init__(self, bet_id: object) -> None:
        super().__init__(
            status_code=400,
            title="Invalid Bet ID",
            message=f"Bet ID '{bet_id}' is not a valid UUID.",
        )


class BetAmountError(HTTPError):
    """
    Raised when the bet amount is invalid (<= 0).
    """

    def __init__(self, amount: object) -> None:
        super().__init__(
            status_code=400,
            title="Invalid Bet Amount",
            message=f"Bet amount '{amount}' must be greater than 0.",
        )


class BetStatusError(HTTPError):
    """
    Raised when the bet status is invalid.
    """

    def __init__(self, status: str) -> None:
        super().__init__(
            status_code=400,
            title="Invalid Bet Status",
            message=f"Bet status '{status}' is not allowed. Must be one of: active, closed, resolved.",
        )


class BetNameError(HTTPError):
    """
    Raised when the bet name is invalid.
    """

    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=400,
            title="Invalid Bet Name",
            message=f"Bet name '{name}' is invalid. It must be at least 3 characters long.",
        )


class BetCoinIdError(HTTPError):
    """
    Raised when the coin ID is invalid.
    """

    def __init__(self, coin_id: object) -> None:
        super().__init__(
            status_code=400,
            title="Invalid Coin ID",
            message=f"Coin ID '{coin_id}' is not valid.",
        )


class BetUserIdError(HTTPError):
    """
    Raised when the user ID is invalid.
    """

    def __init__(self, user_id: object) -> None:
        super().__init__(
            status_code=400,
            title="Invalid User ID",
            message=f"User ID '{user_id}' is not valid.",
        )
