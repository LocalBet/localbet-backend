"""
Test user register domain service.
"""

from datetime import UTC, datetime as real_datetime
from unittest.mock import patch

from pytest import mark, raises as assert_raises

from backend.auth.services import UserRegisterService
from backend.users.errors import UserAlreadyExistsError, UserPasswordMismatchError
from tests.shared.models.mothers import DatetimeMother, WordMother
from tests.users.actions import MockUserActions
from tests.users.models.mothers import UserMother


@mark.unit_testing
def test_user_register() -> None:
    """
    Test user register happy path.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        user_register_service.register(
            id=expected_user.id,
            name=expected_user.name,
            username=expected_user.username,
            email=expected_user.email,
            role_id=expected_user.role_id,
            password=expected_user.password,
            password_verification=expected_user.password,
        )

    user_actions.assert_save_method_called(user=expected_user)


@mark.unit_testing
def test_user_register_password_mismatch() -> None:
    """
    Test user register with password mismatch.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        with assert_raises(expected_exception=UserPasswordMismatchError):
            user_register_service.register(
                id=expected_user.id,
                name=expected_user.name,
                username=expected_user.username,
                email=expected_user.email,
                role_id=expected_user.role_id,
                password=expected_user.password,
                password_verification=WordMother.random(),
            )

        user_actions.assert_save_method_not_called()


@mark.unit_testing
def test_user_register_with_an_existing_user() -> None:
    """
    Test user register with an existing user raises UserAlreadyExistsError.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    user_actions.prepare_user_already_exists_when_saving(
        field="id",
        value=expected_user.id,
    )

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        with assert_raises(expected_exception=UserAlreadyExistsError):
            user_register_service.register(
                id=expected_user.id,
                name=expected_user.name,
                username=expected_user.username,
                email=expected_user.email,
                role_id=expected_user.role_id,
                password=expected_user.password,
                password_verification=expected_user.password,
            )

        user_actions.assert_save_method_called(user=expected_user)


@mark.unit_testing
def test_user_register_with_an_existing_user_email() -> None:
    """
    Test user register with an existing user email raises UserAlreadyExistsError.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    user_actions.prepare_user_already_exists_when_saving(
        field="email",
        value=expected_user.email,
    )

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        with assert_raises(expected_exception=UserAlreadyExistsError):
            user_register_service.register(
                id=expected_user.id,
                name=expected_user.name,
                username=expected_user.username,
                email=expected_user.email,
                role_id=expected_user.role_id,
                password=expected_user.password,
                password_verification=expected_user.password,
            )

        user_actions.assert_save_method_called(user=expected_user)


def test_user_register_with_an_existing_user_username() -> None:
    """
    Test user register with an existing user username raises UserAlreadyExistsError.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    user_actions.prepare_user_already_exists_when_saving(
        field="username",
        value=expected_user.username,
    )

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        with assert_raises(expected_exception=UserAlreadyExistsError):
            user_register_service.register(
                id=expected_user.id,
                name=expected_user.name,
                username=expected_user.username,
                email=expected_user.email,
                role_id=expected_user.role_id,
                password=expected_user.password,
                password_verification=expected_user.password,
            )

        user_actions.assert_save_method_called(user=expected_user)


@mark.unit_testing
@mark.xfail(reason="Role existence check not implemented yet.")
def test_user_register_with_non_existing_role_id() -> None:
    """
    Test user register with a non-existing role ID.
    Currently, since there is no RoleFinderService implemented, this test will pass as the role existence check is
    not performed. This is a placeholder for future implementation.
    """
    user_actions = MockUserActions()
    user_register_service = UserRegisterService(actions=user_actions)

    random_datetime = DatetimeMother.now()
    expected_user = UserMother.create(created_date=random_datetime, updated_date=random_datetime)

    with patch("backend.auth.services.user_register_service.datetime") as mock_dt:
        # Mock datetime.now() to return the expected created_date and updated_date
        mock_dt.now.return_value = random_datetime
        mock_dt.side_effect = real_datetime
        mock_dt.UTC = UTC

        with assert_raises(
            expected_exception=Exception
        ):  # noqa: B017 TODO: Replace Exception with RoleNotFoundError when implemented
            user_register_service.register(
                id=expected_user.id,
                name=expected_user.name,
                username=expected_user.username,
                email=expected_user.email,
                role_id=expected_user.role_id,
                password=expected_user.password,
                password_verification=expected_user.password,
            )

    user_actions.assert_save_method_called(user=expected_user)
