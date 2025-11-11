"""
Test UserPassword value object.
"""

from typing import Any

from pytest import mark, raises as assert_raises

from backend.users.errors import (
    UserPasswordContainsInvalidCharactersError,
    UserPasswordMaxLengthError,
    UserPasswordMinLengthError,
    UserPasswordTypeError,
)
from backend.users.models import UserPassword
from tests.users.models.mothers import UserPasswordMother


@mark.unit_testing
def test_user_password_creation_happy_path() -> None:
    """
    Test successful user password creation with valid password.
    """
    plain_password = UserPasswordMother.random()
    user_password = UserPassword(value=plain_password)

    # Password should be hashed (starts with $argon2id$)
    assert user_password.value.startswith("$argon2id$v=19$m")
    assert user_password.value != plain_password


@mark.unit_testing
def test_user_password_with_mother() -> None:
    """
    Test user password creation using mother.
    """
    user_password = UserPasswordMother.create()
    assert isinstance(user_password.value, str)
    assert user_password.value.startswith("$argon2id$v=19$m")


@mark.unit_testing
def test_user_password_too_short() -> None:
    """
    Test user password with less than minimum length raises error.
    """
    with assert_raises(expected_exception=UserPasswordMinLengthError):
        UserPasswordMother.create(length=7)  # This will create a UserPassword with length 7 (too short)


@mark.unit_testing
def test_user_password_too_long() -> None:
    """
    Test user password with more than maximum length raises error.
    """
    with assert_raises(expected_exception=UserPasswordMaxLengthError):
        UserPasswordMother.create(length=152)  # This will create a UserPassword with length 152 (too long)


@mark.unit_testing
@mark.parametrize("invalid_password", [12345, 12.34, {2: 2}, (1, 2, 3), None, ""])
def test_user_password_not_string(invalid_password: Any) -> None:
    """
    Test user password with non-string type raises error.
    """
    with assert_raises(expected_exception=UserPasswordTypeError):
        UserPassword(value=invalid_password)


@mark.unit_testing
def test_user_password_with_non_printable_characters() -> None:
    """
    Test user password with non-printable characters raises error.
    """
    with assert_raises(expected_exception=UserPasswordContainsInvalidCharactersError):
        UserPasswordMother.create(value="Password123\x00!")


@mark.unit_testing
def test_user_password_equality_with_plain_password() -> None:
    """
    Test user password equality comparison with plain password string.
    """
    plain_password = UserPasswordMother.random()
    user_password = UserPassword(value=plain_password)

    assert user_password == plain_password


@mark.unit_testing
def test_user_password_inequality_with_wrong_plain_password() -> None:
    """
    Test user password inequality with wrong plain password.
    """
    plain_password = UserPasswordMother.random()
    user_password = UserPassword(value=plain_password)

    assert user_password != UserPasswordMother.random()


@mark.unit_testing
def test_user_password_equality_with_another_password_object() -> None:
    """
    Test user password equality with another UserPassword object.
    """
    plain_password = UserPasswordMother.random()
    user_password1 = UserPassword(value=plain_password)
    user_password2 = UserPassword(value=plain_password)

    # They won't be equal because each hash is unique
    assert user_password1 != user_password2


@mark.unit_testing
def test_user_password_equality_with_invalid_type() -> None:
    """
    Test user password equality with invalid type raises NotImplementedError.
    """
    user_password = UserPassword(value="ValidPassword123!")

    with assert_raises(expected_exception=NotImplementedError):
        user_password.__eq__(12345)


@mark.unit_testing
def test_user_password_hash_is_consistent() -> None:
    """
    Test user password hash value is consistent.
    """
    plain_password = UserPasswordMother.random()
    user_password = UserPassword(value=plain_password)

    hash1 = hash(user_password.value)
    hash2 = hash(user_password.value)

    assert hash1 == hash2


@mark.unit_testing
def test_user_password_already_hashed_not_rehashed() -> None:
    """
    Test that already hashed password is not rehashed.
    """
    plain_password = UserPasswordMother.random()
    user_password1 = UserPassword(value=plain_password)
    hashed_value = user_password1.value

    user_password2 = UserPassword(value=hashed_value)

    assert user_password2.value == hashed_value


@mark.unit_testing
def test_user_password_string_representation() -> None:
    """
    Test user password string representation returns hashed value.
    """
    plain_password = UserPasswordMother.random()
    user_password = UserPassword(value=plain_password)

    assert str(user_password) == user_password.value
    assert str(user_password).startswith("$argon2id$v=19$m")


@mark.unit_testing
@mark.parametrize(
    "include_special_chars, include_digits, include_uppercase, include_lowercase",
    [
        (True, True, True, True),
        (True, False, True, True),
        (False, True, True, True),
        (False, False, True, True),
        (True, True, False, True),
        (True, True, True, False),
    ],
)
def test_user_password_with_various_character_combinations(
    include_special_chars: bool, include_digits: bool, include_uppercase: bool, include_lowercase: bool
) -> None:
    """Test user password creation with various character type combinations is valid.

    Tests that passwords can be created with different combinations of:
    - Special characters
    - Digits
    - Uppercase letters
    - Lowercase letters
    """
    user_password = UserPasswordMother.create(
        include_special_chars=include_special_chars,
        include_digits=include_digits,
        include_upper_case=include_uppercase,
        include_lower_case=include_lowercase,
    )

    # Verify the password was created and hashed successfully
    assert isinstance(user_password, UserPassword)
    assert isinstance(user_password.value, str)
    assert user_password.value.startswith("$argon2id$v=19$m")
    assert len(user_password.value) > 0


@mark.unit_testing
def test_user_password_with_spaces() -> None:
    """
    Test user password with spaces is valid.
    """
    UserPasswordMother.create(value="My Secure Password 123!")
    assert True  # If no exception is raised, the test passes


@mark.unit_testing
def test_user_password_with_unicode() -> None:
    """
    Test user password with unicode characters is valid.
    """
    UserPasswordMother.create(value="Pässwörd123!日本語")
    assert True  # If no exception is raised, the test passes


@mark.unit_testing
def test_user_password_hashing_is_unique() -> None:
    """
    Test that same password creates different hashes each time (due to salt).
    """
    plain_password = UserPasswordMother.random()
    user_password1 = UserPassword(value=plain_password)
    user_password2 = UserPassword(value=plain_password)

    assert user_password1.value != user_password2.value
    assert user_password1 == plain_password
    assert user_password2 == plain_password
