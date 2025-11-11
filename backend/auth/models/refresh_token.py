"""
RefreshToken module.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from backend.settings import Settings
from backend.shared.infrastructure.jwa import JWT, JWTSymmetricAlgorithm, JWTType
from backend.users.models import User


class RefreshToken:
    """
    RefreshToken class.
    """

    __algorithm: JWTSymmetricAlgorithm
    __token_type: JWTType
    __issuer: str
    __audience: str
    __subject: str | None  # UUID
    __issued_at_datetime: datetime | None
    __expiration_delta: int | None
    __expiration_datetime: datetime | None
    __not_before_delta: int | None
    __not_before_datetime: datetime | None
    __token_id: str | None  # UUID

    def __init__(self) -> None:
        """
        RefreshToken constructor.
        """
        self.__algorithm = JWTSymmetricAlgorithm.HS256
        self.__token_type = JWTType.REFRESH
        self.__issuer = Settings.APPLICATION_NAME
        self.__audience = Settings.APPLICATION_NAME

    def encode(self, user: User) -> str:
        """
        Encode a refresh JWT token.

        Args:
            user (User): User to encode the token.

        Returns:
            str: Encoded refresh token.
        """
        self.__subject = str(user.id)
        self.__expiration_delta = Settings.REFRESH_TOKEN_EXPIRATION_TIME
        self.__expiration_datetime = datetime.now(tz=UTC) + timedelta(seconds=self.__expiration_delta)
        self.__not_before_delta = Settings.REFRESH_TOKEN_NOT_BEFORE_TIME
        self.__not_before_datetime = datetime.now(tz=UTC) + timedelta(seconds=self.__not_before_delta)
        self.__token_id = str(object=uuid4())

        return JWT.encode_token(
            algorithm=self.__algorithm,
            token_type=self.__token_type,
            secret=Settings.SECRET_KEY,
            issuer=self.__issuer,
            subject=self.__subject,
            audience=self.__audience,
            expiration_delta=self.__expiration_delta,
            not_before_delta=self.__not_before_delta,
            token_id=self.__token_id,
        )

    def decode(self, token: str) -> RefreshToken:
        """
        Decode a refresh JWT token.

        Args:
            token (str): Encoded refresh token.

        Returns:
            RefreshToken: Refresh token.
        """
        decoded_token = JWT.decode_token(
            token=token,
            token_type=self.__token_type,
            secret=Settings.SECRET_KEY,
            issuer=self.__issuer,
            audience=self.__audience,
            accepted_algorithms=[self.__algorithm],
        )

        self.__subject = str(object=UUID(hex=decoded_token["sub"]))
        self.__expiration_datetime = decoded_token["exp"]
        self.__not_before_datetime = decoded_token["nbf"]
        self.__token_id = str(object=UUID(hex=decoded_token["jti"]))

        return self

    @property
    def subject(self) -> str:
        """
        Get the subject (user id).

        Returns:
            str: Subject (user id).
        """
        return self.__subject  # type: ignore[return-value]
