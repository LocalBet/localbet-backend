"""
User domain model.
"""

from datetime import date, datetime
from uuid import UUID, uuid4
from typing_extensions import override

from backend.shared.models import DataModel

from .user_email import UserEmail
from .user_password import UserPassword
from .user_username import UserUsername
from .user_coins import UserCoins


class User(DataModel):
    """
    User model with profile and legal compliance fields.
    """
    __id: UUID

    # Account fields
    __username: UserUsername
    __email: UserEmail
    __password: UserPassword
    __coins: UserCoins
    
    # Profile fields
    __full_name: str | None
    __phone_number: str | None
    __birth_date: date
    __country: str | None
    
    # Legal/compliance fields
    __accepted_terms: bool
    __accepted_privacy_policy: bool
    __is_adult: bool
    __verified_at: datetime | None
    
    # Timestamps
    __created_at: datetime
    __updated_at: datetime

    __hash__ = DataModel.__hash__

    def __init__(
        self,
        *,
        id: UUID | None = None,
        username: str,
        email: str,
        password: str,
        coins: int = 500,
        full_name: str | None = None,
        phone_number: str | None = None,
        birth_date: date,
        country: str | None = None,
        accepted_terms: bool,
        accepted_privacy_policy: bool,
        is_adult: bool,
        verified_at: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """
        User domain model constructor.

        Args:
            username (str): User username.
            email (str): User email.
            password (str): User password.
            coins (int): User available coins (default: 500).
            full_name (str | None): User full name (optional).
            phone_number (str | None): User phone number (optional, None = not provided).
            birth_date (date | None): User birth date.
            country (str | None): User country (optional, None = not provided).
            accepted_terms (bool): Terms and conditions acceptance.
            accepted_privacy_policy (bool): Privacy policy acceptance.
            is_adult (bool): Whether user is 18+ years old.
            verified_at (datetime | None): Verification timestamp (None = pending).
            created_at (datetime | None): Creation timestamp.
            updated_at (datetime | None): Last update timestamp.
        """
        self.__id = id or uuid4()

        self.__username = UserUsername(value=username)
        self.__email = UserEmail(value=email)
        self.__password = UserPassword(value=password)
        self.__coins = UserCoins(value=coins)

        self.__full_name = full_name
        self.__phone_number = phone_number
        self.__birth_date = birth_date
        self.__country = country

        self.__accepted_terms = accepted_terms
        self.__accepted_privacy_policy = accepted_privacy_policy
        self.__is_adult = is_adult
        self.__verified_at = verified_at

        now = datetime.now()
        self.__created_at = created_at or now
        self.__updated_at = updated_at or now

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
    def id(self) -> UUID:
        return self.__id

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
    def coins(self) -> int:
        return int(self.__coins.value)

    @coins.setter
    def coins(self, value: int) -> None:
        self.__coins = UserCoins(value=value)

    def add_coins(self, amount: int) -> None:
        self.coins = self.coins + int(amount)

    def spend_coins(self, amount: int) -> None:
        amount_i = int(amount)
        if self.coins < amount_i:
            raise ValueError("Not enough coins")
        self.coins = self.coins - amount_i

    def check_password(self, plain_password: str) -> bool:
        """
        Checks if the provided password matches the user's password.
        """
        return self.__password == plain_password

    # Profile fields properties
    @property
    def full_name(self) -> str | None:
        return self.__full_name

    @full_name.setter
    def full_name(self, value: str | None) -> None:
        self.__full_name = value

    @property
    def phone_number(self) -> str | None:
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value: str | None) -> None:
        self.__phone_number = value

    @property
    def birth_date(self) -> date:
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, value: date) -> None:
        self.__birth_date = value

    @property
    def country(self) -> str | None:
        return self.__country

    @country.setter
    def country(self, value: str | None) -> None:
        self.__country = value

    # Legal/compliance fields properties (read-only after creation)
    @property
    def accepted_terms(self) -> bool:
        return self.__accepted_terms

    @property
    def accepted_privacy_policy(self) -> bool:
        return self.__accepted_privacy_policy

    @property
    def is_adult(self) -> bool:
        return self.__is_adult

    @property
    def verified_at(self) -> datetime | None:
        return self.__verified_at

    @verified_at.setter
    def verified_at(self, value: datetime | None) -> None:
        self.__verified_at = value

    # Timestamp properties
    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self.__updated_at = value
