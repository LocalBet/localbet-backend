"""
Register a new user service.
"""

from datetime import date

from backend.auth.models import AccessToken, RefreshToken
from backend.users.actions import UserActions
from backend.users.errors import UserPasswordMismatchError
from backend.users.models import User


class UserRegisterService:
    """
    Register a new user service with legal compliance.
    Supports partial registration (identity verification can be completed later).
    """

    __actions: UserActions

    def __init__(self, actions: UserActions) -> None:
        """
        UserRegisterService constructor.

        Args:
            actions (UserActions): User actions.
        """
        self.__actions = actions

    def register(
        self,
        username: str,
        email: str,
        password: str,
        password_verification: str,
        full_name: str | None,
        phone_number: str | None,
        birth_date: date,
        country: str | None,
        accepted_terms: bool,
        accepted_privacy_policy: bool,
    ) -> tuple[str, str]:
        """
        Register a new user with minimal legal compliance.
        Identity verification (phone, country) is optional at registration.

        Args:
            username (str): User username.
            email (str): User email.
            password (str): User password.
            password_verification (str): User password verification.
            full_name (str | None): User full name (optional).
            phone_number (str | None): User phone number (optional, for verification).
            birth_date (date): User birth date (required, must be 18+).
            country (str | None): User country (optional, ISO 2-letter code).
            accepted_terms (bool): Terms acceptance (required, validated by schema).
            accepted_privacy_policy (bool): Privacy policy acceptance (required, validated by schema).

        Raises:
            UserPasswordMismatchError: If passwords don't match.
            UserAlreadyExistsError: If user already exists.

        Returns:
            tuple[str, str]: Access token and refresh token for auto-login.
        """
        self.__ensure_passwords_match(password=password, password_verification=password_verification)
        
        # Legal compliance (terms, privacy, age) already validated by CreateUserSchema
        # No need to re-validate here - trust the schema

        # Age is already validated by CreateUserSchema
        # If we reach here, user is 18+
        is_adult_verified = True

        # Identity verification pending (verified_at = None)
        # User can complete verification later for full access
        user = User(
            username=username,
            email=email,
            password=password,
            coins=1000,
            wins=0,
            losses=0,
            active_groups_count=0,
            full_name=full_name,
            phone_number=phone_number,  # None if not provided (NULL in DB)
            birth_date=birth_date,
            country=country,  # None if not provided (NULL in DB)
            accepted_terms=accepted_terms,
            accepted_privacy_policy=accepted_privacy_policy,
            legal_verified=is_adult_verified,
            verified_at=None,  # Identity verification pending
        )

        self.__actions.save(user=user)

        # TODO: Create initial wallet transaction
        # from backend.users.models import WalletTransaction
        # initial_transaction = WalletTransaction(
        #     user_id=user.id,
        #     amount=1000,
        #     transaction_type='initial_balance',
        #     description='Saldo inicial al registrarse'
        # )
        # self.__wallet_actions.save_transaction(transaction=initial_transaction)

        # Generate tokens for auto-login
        access_token = AccessToken().encode(user=user)
        refresh_token = RefreshToken().encode(user=user)

        return access_token, refresh_token

    def __ensure_passwords_match(self, password: str, password_verification: str) -> None:
        """
        Ensure that the password and the password verification match.
        """
        if password != password_verification:
            raise UserPasswordMismatchError()
