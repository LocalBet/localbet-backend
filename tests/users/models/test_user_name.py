"""
Test UserName value object.
"""

from pytest import mark, raises as assert_raises

from backend.users.errors import (
    UserNameContainsInvalidCharactersError,
    UserNameMaxLengthError,
    UserNameMinLengthError,
    UserNameTypeError,
)
from backend.users.models import UserName
from tests.users.models.mothers import UserNameMother


@mark.unit_testing
def test_user_name_creation_happy_path() -> None:
    """
    Test successful user name creation with valid name.
    """
    name = "John Doe"
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_with_mother() -> None:
    """
    Test user name creation using mother.
    """
    user_name = UserNameMother.create()

    assert isinstance(user_name.value, str)
    assert len(user_name.value) >= 3
    assert len(user_name.value) <= 128


@mark.unit_testing
def test_user_name_minimum_length() -> None:
    """
    Test user name with minimum valid length (3 characters).
    """
    name = "Bob"  # Exactly 3 characters
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_too_short() -> None:
    """
    Test user name with less than minimum length raises error.
    """
    name = "Ab"  # 2 characters, too short

    with assert_raises(expected_exception=UserNameMinLengthError):
        UserName(value=name)


@mark.unit_testing
def test_user_name_maximum_length() -> None:
    """
    Test user name with maximum valid length (128 characters).
    """
    name = "A" * 128  # Exactly 128 characters
    user_name = UserName(value=name)

    assert user_name.value == name
    assert len(user_name.value) == 128


@mark.unit_testing
def test_user_name_too_long() -> None:
    """
    Test user name with more than maximum length raises error.
    """
    name = "A" * 129  # 129 characters, too long

    with assert_raises(expected_exception=UserNameMaxLengthError):
        UserName(value=name)


@mark.unit_testing
def test_user_name_not_string() -> None:
    """
    Test user name with non-string type raises error.
    """
    with assert_raises(expected_exception=UserNameTypeError):
        UserName(value=12345)  # type: ignore[arg-type]


@mark.unit_testing
def test_user_name_none_value() -> None:
    """
    Test user name with None value raises error.
    """
    with assert_raises(expected_exception=UserNameTypeError):
        UserName(value=None)  # type: ignore[arg-type]


@mark.unit_testing
def test_user_name_with_leading_whitespace() -> None:
    """
    Test user name with leading whitespace raises error.
    """
    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        UserName(value="  John Doe")


@mark.unit_testing
def test_user_name_with_trailing_whitespace() -> None:
    """
    Test user name with trailing whitespace raises error.
    """
    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        UserName(value="John Doe  ")


@mark.unit_testing
def test_user_name_with_non_printable_characters() -> None:
    """
    Test user name with non-printable characters raises error.
    """
    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        UserName(value="John\x00Doe")


@mark.unit_testing
def test_user_name_with_tab_character() -> None:
    """
    Test user name with tab character raises error.
    """
    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        UserName(value="John\tDoe")


@mark.unit_testing
def test_user_name_with_newline_character() -> None:
    """
    Test user name with newline character raises error.
    """
    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        UserName(value="John\nDoe")


@mark.unit_testing
def test_user_name_equality() -> None:
    """
    Test two user names with same value are equal.
    """
    name = "John Doe"
    user_name1 = UserName(value=name)
    user_name2 = UserName(value=name)

    assert user_name1 == user_name2


@mark.unit_testing
def test_user_name_inequality() -> None:
    """
    Test two user names with different values are not equal.
    """
    user_name1 = UserName(value="John Doe")
    user_name2 = UserName(value="Jane Smith")

    assert user_name1 != user_name2


@mark.unit_testing
def test_user_name_hash() -> None:
    """
    Test user name hash works correctly for set operations.
    """
    name = "John Doe"
    user_name1 = UserName(value=name)
    user_name2 = UserName(value=name)

    assert hash(user_name1) == hash(user_name2)

    # Can be used in sets
    name_set = {user_name1, user_name2}
    assert len(name_set) == 1


@mark.unit_testing
def test_user_name_string_representation() -> None:
    """
    Test user name string representation.
    """
    name = "John Doe"
    user_name = UserName(value=name)

    assert str(user_name) == name


@mark.unit_testing
def test_user_name_with_special_characters() -> None:
    """
    Test user name with special printable characters is valid.
    """
    name = "O'Brien-Smith"
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_with_numbers() -> None:
    """
    Test user name with numbers is valid.
    """
    name = "John Doe 123"
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_with_unicode_characters() -> None:
    """
    Test user name with unicode characters is valid.
    """
    name = "José García"
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_with_emoji() -> None:
    """
    Test user name with emoji is valid (printable unicode).
    """
    name = "John Doe 😊"
    user_name = UserName(value=name)

    assert user_name.value == name


@mark.unit_testing
def test_user_name_empty_string() -> None:
    """
    Test user name with empty string raises min length error.
    """
    with assert_raises(expected_exception=UserNameMinLengthError):
        UserName(value="")
