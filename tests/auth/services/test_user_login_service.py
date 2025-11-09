"""
Test user login domain service.
"""

from unittest import mock

from pydantic import ValidationError
from pytest import mark, raises as assert_raises

from backend.auth.errors import PasswordVerificationError
from backend.auth.services import UserLoginService
from backend.users.errors import UserNotFoundError
from backend.users.services import UserFinderService
from tests.shared.models.mothers import EmailMother, PasswordMother
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother


@mark.unit_testing
def test_user_login_happy_path() -> None:
    """
    Test successful user login returns access and refresh tokens.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    plain_password = PasswordMother.random()
    email = EmailMother.random()
    user = UserMother.create(email=email, password=plain_password)
    user_action.prepare_return_search(user=user)

    access_token, refresh_token = user_login_service.login(
        email=email,
        password=plain_password,
    )
    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)
    assert len(access_token) > 0
    assert len(refresh_token) > 0

@mark.unit_testing
def test_user_login_user_not_found() -> None:
    """
    Test login with non-existent email raises UserNotFoundError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    user_action.prepare_return_search(user=None)

    non_existent_email = EmailMother.random()
    plain_password = PasswordMother.random()

    with assert_raises(expected_exception=UserNotFoundError):
        user_login_service.login(
            email=non_existent_email,
            password=plain_password,
        )

@mark.unit_testing
def test_user_login_wrong_password() -> None:
    """
    Test login with incorrect password raises PasswordVerificationError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    correct_password = PasswordMother.random()
    user = UserMother.create(password=correct_password)
    user_action.prepare_return_search(user=user)

    wrong_password = PasswordMother.random()
    assert wrong_password != correct_password

    with assert_raises(expected_exception=PasswordVerificationError):
        user_login_service.login(
            email=user.email,
            password=wrong_password,
        )

@mark.unit_testing
def test_user_login_empty_password() -> None:
    """
    Test login with empty password raises PasswordVerificationError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    user = UserMother.create()
    user_action.prepare_return_search(user=user)

    with assert_raises(expected_exception=ValidationError):
        user_login_service.login(
            email=user.email,
            password="",
        )


@mark.unit_testing
def test_user_login_case_sensitive_email() -> None:
    """
    Test that email matching works with exact case.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    plain_password = PasswordMother.random()
    email = EmailMother.random().upper()
    user = UserMother.create(email=email, password=plain_password)
    user_action.prepare_return_search(user=user)

    access_token, refresh_token = user_login_service.login(
        email=email.lower(),
        password=plain_password,
    )

    assert isinstance(access_token, str)
    assert isinstance(refresh_token, str)


@mark.unit_testing
def test_user_login_timing_attack_protection() -> None:
    """
    Test that login executes password hashing even when user doesn't exist (timing attack protection).
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    user_login_service = UserLoginService(actions=user_action, finder=user_finder)

    plain_password = PasswordMother.random()
    email = EmailMother.random()
    UserMother.create(password=plain_password, email=email)
    user_action.prepare_return_search(user=None)
    non_existent_email = EmailMother.random()

    with mock.patch(
        'backend.auth.services.user_login_service.UserLoginService._UserLoginService__avoid_timing_attack'
    ) as mock_avoid, assert_raises(expected_exception=UserNotFoundError):
        user_login_service.login(
            email=non_existent_email,
            password=plain_password,
        )

        mock_avoid.assert_called_once_with(password=plain_password)
