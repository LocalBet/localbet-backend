"""
Test refresh access token domain service.
"""

from json import JSONDecodeError
from unittest import mock

from pytest import mark, raises as assert_raises

from backend.auth.errors import InvalidRefreshTokenError
from backend.auth.models import RefreshToken
from backend.auth.services import RefreshAccessTokenService
from backend.users.services import UserFinderService
from tests.shared.models.mothers import WordMother
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother


@mark.unit_testing
def test_refresh_access_token_happy_path() -> None:
    """
    Test successful refresh returns new access token and same refresh token.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    user = UserMother.create()
    user_action.prepare_return_search(user=user)

    # Generate a valid refresh token for the user
    valid_refresh_token = RefreshToken().encode(user=user)

    new_access_token, returned_refresh_token = refresh_service.refresh(refresh_token=valid_refresh_token)

    assert isinstance(new_access_token, str)
    assert len(new_access_token) > 0
    assert returned_refresh_token == valid_refresh_token


@mark.unit_testing
def test_refresh_access_token_invalid_token_format() -> None:
    """
    Test refresh with malformed token raises InvalidRefreshTokenError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    invalid_token = WordMother.random()

    with assert_raises(expected_exception=InvalidRefreshTokenError):
        refresh_service.refresh(refresh_token=invalid_token)


@mark.unit_testing
def test_refresh_access_token_user_not_found() -> None:
    """
    Test refresh with valid token but user no longer exists raises InvalidRefreshTokenError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    user = UserMother.create()
    valid_refresh_token = RefreshToken().encode(user=user)

    user_action.prepare_return_search(user=None)

    with assert_raises(expected_exception=InvalidRefreshTokenError):
        refresh_service.refresh(refresh_token=valid_refresh_token)


@mark.unit_testing
def test_refresh_access_token_empty_token() -> None:
    """
    Test refresh with empty token raises InvalidRefreshTokenError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    with assert_raises(expected_exception=InvalidRefreshTokenError):
        refresh_service.refresh(refresh_token="")


@mark.unit_testing
def test_refresh_access_token_decode_exception() -> None:
    """
    Test that any exception during token decode is caught and raises InvalidRefreshTokenError.
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    user = UserMother.create()
    valid_token = RefreshToken().encode(user=user)

    # Mock the decode to raise an exception
    with mock.patch(
        "backend.auth.services.refresh_access_token_service.RefreshToken.decode",
        side_effect=JSONDecodeError(msg="Decode failed", doc="", pos=0),
    ), assert_raises(expected_exception=InvalidRefreshTokenError):
        refresh_service.refresh(refresh_token=valid_token)


@mark.unit_testing
def test_refresh_access_token_returns_same_refresh_token() -> None:
    """
    Test that refresh returns the same refresh token (not a new one).
    """
    user_action = MockUserActions()
    user_finder = UserFinderService(action=user_action)
    refresh_service = RefreshAccessTokenService(action=user_action, user_finder=user_finder)

    user = UserMother.create()
    user_action.prepare_return_search(user=user)

    original_refresh_token = RefreshToken().encode(user=user)

    _, returned_refresh_token = refresh_service.refresh(refresh_token=original_refresh_token)

    # Verify the same refresh token is returned
    assert returned_refresh_token == original_refresh_token
