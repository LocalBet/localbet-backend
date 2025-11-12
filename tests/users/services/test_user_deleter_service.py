"""
Test user deleter domain service.
"""

from pytest import mark, raises as assert_raises

from backend.auth.errors import PasswordVerificationError
from backend.users.errors import UserNotFoundError
from backend.users.services import UserDeleterService
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother, UserPasswordMother


@mark.unit_testing
def test_user_deleter() -> None:
    """
    Test user deleter happy path.
    """
    user_actions = MockUserActions()
    use_case = UserDeleterService(action=user_actions)

    password = UserPasswordMother.unhashed()
    user_to_delete = UserMother.create(password=password)

    use_case.delete(user=user_to_delete, password=password)
    user_actions.assert_delete_method_called(user=user_to_delete)


@mark.unit_testing
def test_user_deleter_with_a_nonexisting_user() -> None:
    """
    Test that deleting a non-existing user raises a UserNotFoundError.
    """
    user_actions = MockUserActions()
    user_deleter_service = UserDeleterService(action=user_actions)

    password = UserPasswordMother.unhashed()
    user_to_delete = UserMother.create(password=password)
    user_actions.prepare_user_not_found_when_deleting(user=user_to_delete)

    with assert_raises(
        expected_exception=UserNotFoundError,
        match=f"User with <<<id>>> <<<{user_to_delete.id}>>> was not found.",
    ):
        user_deleter_service.delete(user=user_to_delete, password=password)

    user_actions.assert_delete_method_called(user=user_to_delete)


@mark.unit_testing
def test_user_deleter_with_invalid_password() -> None:
    """
    Test that deleting a user with an invalid password should raise a PasswordVerificationError.
    """
    user_actions = MockUserActions()
    user_deleter_service = UserDeleterService(action=user_actions)

    user_to_delete = UserMother.create()

    with assert_raises(
        expected_exception=PasswordVerificationError,
        match=r"The provided password does not match the user's password.",
    ):
        user_deleter_service.delete(user=user_to_delete, password=UserPasswordMother.unhashed())

    user_actions.assert_delete_method_not_called()
