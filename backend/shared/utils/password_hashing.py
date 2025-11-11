"""
Password hashing utilities.
"""

from enum import StrEnum, unique
from secrets import SystemRandom
from typing import Annotated

from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError
from pydantic import Field, validate_call

ALPHABET_LOWERCASE_BASIC: str = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UPPERCASE_BASIC: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS_BASIC: str = "0123456789"
ALPHABET_BASIC: str = ALPHABET_LOWERCASE_BASIC + ALPHABET_UPPERCASE_BASIC + DIGITS_BASIC


@unique
class KDFAlgorithm(StrEnum):
    """
    Key Derivation Function algorithms.
    Suitable for password hashing.
    """

    ARGON2I = "argon2i"
    ARGON2D = "argon2d"
    ARGON2ID = "argon2id"


def random_salt() -> str:
    """
    Generates a random salt of the specified length using the basic alphabet (lowercase, uppercase, digits).
    By default, the length is 32 characters.

    Raises:
        ValueError: If length is less than 1.
    Returns:
        str: The generated random salt.
    """
    return "".join(SystemRandom().choice(seq=ALPHABET_BASIC) for _ in range(32))


@validate_call
def password_hashing(
    data: Annotated[
        str,
        Field(
            default=...,
            min_length=1,
            description="The data to hash.",
            examples=["data"],
            strict=True,
        ),
    ],
    kdf_algorithm: Annotated[
        KDFAlgorithm,
        Field(
            default=KDFAlgorithm.ARGON2ID,
            description="The KDF algorithm to use for hashing. This is only for password hashing purposes.",
            examples=[KDFAlgorithm.ARGON2ID],
        ),
    ] = KDFAlgorithm.ARGON2ID,
    salt: Annotated[
        str | None,
        Field(
            min_length=1,
            description="The salt to use.",
            examples=["salt123"],
            strict=True,
        ),
    ] = None,
) -> str:
    """
    Hashes the provided data using the hashing algorithm provided. If no salt is provided, no salt will be used.
    If data or salt are strings, it will be converted to bytes using utf-8.

    Args:
        data (str): The data to hash.
        kdf_algorithm (KDFAlgorithm): The KDF algorithm to use for hashing. This is only for password hashing purposes.
            Defaults to KDFAlgorithm.ARGON2ID.
        salt (str, optional): The salt to use. Defaults to None.

    Warnings:
        UserWarning: If salt is provided, it is recommended to not use hashers for password hashing.

    Raises:
        ValidationError: If hashing_algorithm is not of type HashingAlgorithm.
        ValidationError: If data is not of type str.
        ValidationError: If data is empty.
        ValidationError: If salt is not of type str.
        ValidationError: If salt is empty.

    Returns:
        str: The hashed data.

    Return format:
        ${md5}${salt}${new_hash}
        ${sha1}${salt}${new_hash}
        ${sha224}${salt}${new_hash}
        ${sha256}${salt}${new_hash}
        ${sha384}${salt}${new_hash}
        ${sha512}${salt}${new_hash}
        ${sha3_224}${salt}${new_hash}
        ${sha3_256}${salt}${new_hash}
        ${sha3_384}${salt}${new_hash}
        ${sha3_512}${salt}${new_hash}
        ${blake2b}${salt}${new_hash}
        ${blake2s}${salt}${new_hash}
    """
    if kdf_algorithm == KDFAlgorithm.ARGON2ID:
        return PasswordHasher(type=Type.ID).hash(
            password=bytes(data, encoding="utf-8"),
            salt=bytes(salt if salt is not None else random_salt(), encoding="utf-8"),
        )

    if kdf_algorithm == KDFAlgorithm.ARGON2D:
        return PasswordHasher(type=Type.D).hash(
            password=bytes(data, encoding="utf-8"),
            salt=bytes(salt if salt is not None else random_salt(), encoding="utf-8"),
        )

    if kdf_algorithm == KDFAlgorithm.ARGON2I:
        return PasswordHasher(type=Type.I).hash(
            password=bytes(data, encoding="utf-8"),
            salt=bytes(salt if salt is not None else random_salt(), encoding="utf-8"),
        )


@validate_call
def compare_passwords(
    *,
    plain_password: Annotated[
        str,
        Field(
            default=...,
            min_length=1,
            description="The plain password.",
            examples=["password123"],
            strict=True,
        ),
    ],
    hashed_password: Annotated[
        str,
        Field(
            default=...,
            min_length=1,
            description="The hashed password.",
            examples=[
                "$argon2id$v=19$m=47104,t=1,p=5$UkN4OGpkSDVsd1pqUXdOY3Nyd3kwUHlzSm5HNWJBZ3g$j6/mFJz8yeDfX2ka4FDELP8HJl8VwyJH7vURmT8iyKg"
            ],
            strict=True,
        ),
    ],
) -> bool:
    """
    Compares a plain password to a hashed password to see if they are identical.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Raises:
        ValidationError: If plain_password is not an string.
        ValidationError: If plain_password is empty.
        ValidationError: If hashed_password is not an string.
        ValidationError: If hashed_password is empty.

    Returns:
        bool: True if the passwords are identical, False otherwise.
    """
    try:
        return PasswordHasher().verify(
            hash=hashed_password.encode(encoding="utf-8"),
            password=plain_password.encode(encoding="utf-8"),
        )

    except VerifyMismatchError:
        return False
