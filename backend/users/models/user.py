"""
User domain model.
"""

from typing_extensions import override

from backend.shared.models import DataModel

from .user_email import UserEmail
from .user_password import UserPassword
from .user_username import UserUsername
from .user_coins import UserCoins


class User(DataModel):
    """
    User model (simplified).
    Includes: username, email, password, coins.
    """

    __username: UserUsername
    __email: UserEmail
    __password: UserPassword
    __coins: UserCoins

    __hash__ = DataModel.__hash__

    def __init__(self, username: str, email: str, password: str, coins: float = 0) -> None:
        """
        User domain model constructor.

        Args:
            username (str): User username.
            email (str): User email.
            password (str): User password.
            coins (float): User available coins.
        """
        self.__username = UserUsername(value=username)
        self.__email = UserEmail(value=email)
        self.__password = UserPassword(value=password)
        self.__coins = UserCoins(value=coins)

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the user is equal to another user.
        We exclude password because it may be hashed/salted.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        self_dict = self.to_dict()
        self_dict.pop("password", None)

        other_dict = other.to_dict()
        other_dict.pop("password", None)

        return self_dict == other_dict

    @property
    def username(self) -> str:
        return self.__username.value

    @username.setter
    def username(self, value: str) -> None:
        self.__username = UserUsername(value=value)

    @property
    def email(self) -> str:
        return self.__email.value

    @email.setter
    def email(self, value: str) -> None:
        self.__email = UserEmail(value=value)

    @property
    def password(self) -> str:
        return self.__password.value

    @password.setter
    def password(self, value: str) -> None:
        self.__password = UserPassword(value=value)

    @property
    def coins(self) -> float:
        return float(self.__coins.value)

    @coins.setter
    def coins(self, value: float) -> None:
        self.__coins = UserCoins(value=value)

    def add_coins(self, amount: float) -> None:
        self.coins = self.coins + float(amount)

    def spend_coins(self, amount: float) -> None:
        amount_f = float(amount)
        if self.coins < amount_f:
            raise ValueError("Not enough coins")
        self.coins = self.coins - amount_f

    def check_password(self, plain_password: str) -> bool:
        """
        Checks if the provided password matches the user's password.
        """
        return self.__password == plain_password
