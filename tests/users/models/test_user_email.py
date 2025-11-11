"""
Test UserEmail value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from backend.users.errors import UserEmailMaxLengthError, UserEmailMinLengthError, UserEmailTypeError
from backend.users.models import UserEmail
from tests.shared.models.mothers import WordMother
from tests.users.models.mothers import UserEmailMother


@mark.unit_testing
def test_user_email_creation_happy_path() -> None:
    """
    Test successful user email creation with valid email.
    """
    email = UserEmailMother.random()
    user_email = UserEmail(value=email)

    assert user_email.value == email


@mark.unit_testing
def test_user_email_with_mother() -> None:
    """
    Test user email creation using mother.
    """
    user_email = UserEmailMother.create()

    assert isinstance(user_email.value, str)
    assert "@" in user_email.value
    assert "." in user_email.value.split("@")[-1]

@mark.unit_testing
def test_user_email_too_short() -> None:
    """
    Test user email with less than minimum length raises error.
    """
    email = WordMother.of_length(length=1) + "@."
    with assert_raises(expected_exception=UserEmailMinLengthError):
        UserEmail(value=email)


@mark.unit_testing
def test_user_email_maximum_length() -> None:
    """
    Test user email with maximum valid length (150 characters).
    """
    local_part = WordMother.of_length(length=150)
    email = f"{local_part}@example.com"

    with assert_raises(expected_exception=UserEmailMaxLengthError):
        UserEmail(value=email)

@mark.unit_testing
def test_user_email_missing_at_symbol() -> None:
    """
    Test user email without @ symbol raises error.
    """
    with assert_raises(expected_exception=UserEmailTypeError):
        UserEmail(value=WordMother.random() + "invalidemailcom")


@mark.unit_testing
def test_user_email_missing_dot_after_at() -> None:
    """
    Test user email without dot after @ symbol raises error.
    """
    with assert_raises(expected_exception=UserEmailTypeError):
        UserEmail(value=WordMother.random() + "@invalidemailcom")


@mark.unit_testing
@mark.parametrize("invalid_value", [12345, None, "", {}, []])
def test_user_email_not_string(invalid_value: Any) -> None:
    """
    Test user email with non-string type raises error.
    """
    with assert_raises(expected_exception=UserEmailTypeError):
        UserEmail(value=invalid_value)

@mark.unit_testing
def test_user_email_equality() -> None:
    """
    Test two user emails with same value are equal.
    """
    email = UserEmailMother.random()
    user_email1 = UserEmail(value=email)
    user_email2 = UserEmail(value=email)

    assert user_email1 == user_email2


@mark.unit_testing
def test_user_email_inequality() -> None:
    """
    Test two user emails with different values are not equal.
    """
    user_email1 = UserEmail(value=UserEmailMother.random())
    user_email2 = UserEmail(value=user_email1.value + "x")

    assert user_email1 != user_email2


@mark.unit_testing
def test_user_email_hash() -> None:
    """
    Test user email hash works correctly for set operations.
    """
    user_email1 = UserEmail(value=UserEmailMother.random())
    user_email2 = UserEmail(value=user_email1.value)

    assert hash(user_email1) == hash(user_email2)


@mark.unit_testing
def test_user_email_string_representation() -> None:
    """
    Test user email string representation.
    """
    user_email = UserEmail(value=UserEmailMother.random())

    assert str(user_email) == user_email.value


@mark.unit_testing
def test_user_email_with_subdomain() -> None:
    """
    Test user email with subdomain is valid.
    """
    UserEmailMother.with_subdomain()
    assert True  # If no exception is raised, the test passes


@mark.unit_testing
def test_user_email_with_plus_sign() -> None:
    """
    Test user email with plus sign is valid.
    """
    UserEmailMother.with_plus_sign()
    assert True  # If no exception is raised, the test passes

@mark.unit_testing
def test_user_email_with_dots() -> None:
    """
    Test user email with dots in local part is valid.
    """
    UserEmailMother.with_dots_in_local_part()
    assert True  # If no exception is raised, the test passes
