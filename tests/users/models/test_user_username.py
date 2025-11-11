"""
Test UserUsername value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from backend.users.errors import (
    UserUsernameContainsInvalidCharactersError,
    UserUsernameMaxLengthError,
    UserUsernameMinLengthError,
    UserUsernameTypeError,
    UserUsernameUppercaseError,
)
from backend.users.models import UserUsername
from tests.users.models.mothers import UserUsernameMother


@mark.unit_testing
def test_user_username_creation_happy_path() -> None:
    """
    Test successful user username creation with valid username.
    """
    username = UserUsernameMother.of_length(length=10)
    user_username = UserUsername(value=username)

    assert user_username.value == username


@mark.unit_testing
def test_user_username_with_mother() -> None:
    """
    Test user username creation using mother.
    """
    user_username = UserUsernameMother.of_length(length=10)

    assert isinstance(user_username, str)
    assert len(user_username) == 10
    assert user_username.islower()


@mark.unit_testing
def test_user_username_minimum_length() -> None:
    """
    Test user username with minimum valid length (3 characters).
    """
    username = UserUsernameMother.of_length(length=3)
    user_username = UserUsername(value=username)

    assert user_username.value == username


@mark.unit_testing
def test_user_username_too_short() -> None:
    """
    Test user username with less than minimum length raises error.
    """
    username = UserUsernameMother.of_length(length=2)

    with assert_raises(expected_exception=UserUsernameMinLengthError):
        UserUsername(value=username)


@mark.unit_testing
def test_user_username_maximum_length() -> None:
    """
    Test user username with maximum valid length (32 characters).
    """
    username = UserUsernameMother.of_length(length=32)
    user_username = UserUsername(value=username)

    assert user_username.value == username
    assert len(user_username.value) == 32


@mark.unit_testing
def test_user_username_too_long() -> None:
    """
    Test user username with more than maximum length raises error.
    """
    username = UserUsernameMother.of_length(length=33)

    with assert_raises(expected_exception=UserUsernameMaxLengthError):
        UserUsername(value=username)


@mark.unit_testing
@mark.parametrize("invalid_value", [123, 45.67, [], {}, (), True, False, None])
def test_user_username_not_string(invalid_value: Any) -> None:
    """
    Test user username with non-string type raises error.
    """
    with assert_raises(expected_exception=UserUsernameTypeError):
        UserUsername(value=invalid_value)


@mark.unit_testing
def test_user_username_with_uppercase() -> None:
    """
    Test user username with uppercase characters raises error.
    """
    with assert_raises(expected_exception=UserUsernameUppercaseError):
        UserUsername(value=UserUsernameMother.some_uppercase())


@mark.unit_testing
def test_user_username_with_special_characters() -> None:
    """
    Test user username with special characters (not alphanumeric or underscore) raises error.
    """
    with assert_raises(expected_exception=UserUsernameContainsInvalidCharactersError):
        UserUsername(value=UserUsernameMother.invalid_value())


@mark.unit_testing
def test_user_username_empty_string() -> None:
    """
    Test user username with empty string raises min length error.
    """
    with assert_raises(expected_exception=UserUsernameMinLengthError):
        UserUsername(value="")


@mark.unit_testing
def test_user_username_equality() -> None:
    """
    Test two user usernames with same value are equal.
    """
    username = UserUsernameMother.random()
    user_username1 = UserUsername(value=username)
    user_username2 = UserUsername(value=username)

    assert user_username1 == user_username2


@mark.unit_testing
def test_user_username_inequality() -> None:
    """
    Test two user usernames with different values are not equal.
    """
    user_username1 = UserUsernameMother.random()
    user_username2 = UserUsernameMother.create(value=user_username1 + "x")

    assert user_username1 != user_username2


@mark.unit_testing
def test_user_username_hash() -> None:
    """
    Test user username hash works correctly for set operations.
    """
    username = UserUsernameMother.random()

    user_username1 = UserUsername(value=username)
    user_username2 = UserUsername(value=username)

    assert hash(user_username1) == hash(user_username2)

    username_set = {user_username1, user_username2}
    assert len(username_set) == 1


@mark.unit_testing
def test_user_username_ends_with_underscore() -> None:
    """
    Test user username ending with underscore is valid.
    """
    username = "username_"
    user_username = UserUsername(value=username)

    assert user_username.value == username
