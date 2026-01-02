"""
Bet image_url value object.
"""

from backend.shared.models import ValueObject


class BetImageUrl(ValueObject[str | None]):
    """
    Bet image_url value object (optional).
    """

    def _validate(self, value: str | None) -> None:
        if value is not None and len(value) > 500:
            raise ValueError("Image URL cannot exceed 500 characters")
