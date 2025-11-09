"""
Test user update domain service.
"""

from pytest import mark, raises as assert_raises

from backend.auth.errors import PasswordVerificationError
from backend.users.errors import (
    UserNameContainsInvalidCharactersError,
    UserPasswordMismatchError,
    UserUpdatePasswordError,
    UserUsernameContainsInvalidCharactersError,
)
from backend.users.services import UserUpdateService
from tests.shared.models.mothers import EmailMother, WordMother
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother, UserNameMother, UserPasswordMother, UserUsernameMother


@mark.unit_testing
def test_user_update_username() -> None:
    """
    Test user update username.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    new_username = UserUsernameMother.of_length(length=4)

    user_update_service.update(user=user, username=new_username)

    assert user.username == new_username
    user_actions.assert_update_method_called(user=user)


@mark.unit_testing
def test_user_update_with_invalid_username() -> None:
    """
    Test user update with invalid username raises ValidationError.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    invalid_username = UserUsernameMother.invalid_value()

    with assert_raises(expected_exception=UserUsernameContainsInvalidCharactersError):
        user_update_service.update(user=user, username=invalid_username)

    user_actions.assert_update_method_not_called()


@mark.unit_testing
def test_user_update_email() -> None:
    """
    Test user update email.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    new_email = f"{WordMother.random()}@example.com"

    user_update_service.update(user=user, email=new_email)

    assert user.email == new_email
    user_actions.assert_update_method_called(user=user)


@mark.unit_testing
def test_user_update_name() -> None:
    """
    Test user update name.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    new_name = UserNameMother.of_length(length=4)

    user_update_service.update(user=user, name=new_name)

    assert user.name == new_name
    user_actions.assert_update_method_called(user=user)

@mark.unit_testing
def test_user_update_name_with_invalid_value() -> None:
    """
    Test user update name with invalid value raises ValidationError.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    invalid_name = UserNameMother.invalid_value()

    with assert_raises(expected_exception=UserNameContainsInvalidCharactersError):
        user_update_service.update(user=user, name=invalid_name)

    user_actions.assert_update_method_not_called()


@mark.unit_testing
def test_user_update_password() -> None:
    """
    Test user update password with correct old password.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    old_password = UserPasswordMother.random()
    user = UserMother.create(password=old_password)
    new_password = UserPasswordMother.random()

    user_update_service.update(
        user=user,
        old_password=old_password,
        new_password=new_password,
        new_password_confirmation=new_password,
    )

    assert user.check_password(plain_password=new_password)
    user_actions.assert_update_method_called(user=user)


@mark.unit_testing
def test_user_update_password_with_wrong_old_password() -> None:
    """
    Test user update password with wrong old password raises PasswordVerificationError.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    old_password = UserPasswordMother.random()
    user = UserMother.create(password=old_password)
    wrong_old_password = UserPasswordMother.random()
    new_password = UserPasswordMother.random()

    with assert_raises(expected_exception=PasswordVerificationError):
        user_update_service.update(
            user=user,
            old_password=wrong_old_password,
            new_password=new_password,
            new_password_confirmation=new_password,
        )

    user_actions.assert_update_method_not_called()


@mark.unit_testing
def test_user_update_password_with_mismatched_confirmation() -> None:
    """
    Test user update password with mismatched new password and confirmation raises UserPasswordMismatchError.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    old_password = UserPasswordMother.random()
    user = UserMother.create(password=old_password)
    new_password = UserPasswordMother.random()
    wrong_confirmation = UserPasswordMother.random()

    with assert_raises(expected_exception=UserPasswordMismatchError):
        user_update_service.update(
            user=user,
            old_password=old_password,
            new_password=new_password,
            new_password_confirmation=wrong_confirmation,
        )

    user_actions.assert_update_method_not_called()


@mark.unit_testing
def test_user_update_password_with_incomplete_fields() -> None:
    """
    Test user update password with incomplete password fields raises UserUpdatePasswordError.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    new_password = UserPasswordMother.random()

    with assert_raises(expected_exception=UserUpdatePasswordError):
        user_update_service.update(user=user, new_password=new_password)

    user_actions.assert_update_method_not_called()


@mark.unit_testing
def test_user_update_multiple_fields() -> None:
    """
    Test user update multiple fields at once.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()
    new_username = UserUsernameMother.of_length(length=4)
    new_email = EmailMother.random()
    new_name = WordMother.random()

    user_update_service.update(user=user, username=new_username, email=new_email, name=new_name)

    assert user.username == new_username
    assert user.email == new_email
    assert user.name == new_name
    user_actions.assert_update_method_called(user=user)


@mark.unit_testing
def test_user_update_no_changes() -> None:
    """
    Test user update with no changes does not call update action.
    """
    user_actions = MockUserActions()
    user_update_service = UserUpdateService(action=user_actions)

    user = UserMother.create()

    user_update_service.update(user=user)

    user_actions.assert_update_method_not_called()

