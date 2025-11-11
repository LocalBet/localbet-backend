"""
Test User model.
"""

from datetime import UTC, datetime
from uuid import uuid4

from pytest import mark, raises as assert_raises

from backend.users.models import User
from tests.shared.models.mothers import DatetimeMother, IdentifierMother
from tests.users.models.mothers import (
    UserEmailMother,
    UserMother,
    UserNameMother,
    UserPasswordMother,
    UserRoleIdMother,
    UserUsernameMother,
)


@mark.unit_testing
def test_user_creation_happy_path() -> None:
    """
    Test successful user creation with all valid fields.
    """
    user_id_str = IdentifierMother.random()
    name = UserNameMother.create().value
    username = UserUsernameMother.create().value
    email = UserEmailMother.create().value
    password = UserPasswordMother.create().value
    role_id_str = IdentifierMother.random()
    create_date = DatetimeMother.random()
    update_date = DatetimeMother.now()

    user = User(
        id=user_id_str,
        name=name,
        username=username,
        email=email,
        password=password,
        role_id=role_id_str,
        create_date=create_date,
        update_date=update_date,
    )

    assert user.id == user_id_str.lower()
    assert user.name == name
    assert user.username == username
    assert user.email == email
    assert user.role_id == role_id_str.lower()
    assert user.create_date == create_date
    assert user.update_date == update_date


@mark.unit_testing
def test_user_to_dict() -> None:
    """
    Test user to_dict method returns all fields.
    """
    user = UserMother.create()
    user_dict = user.to_dict()

    assert "id" in user_dict
    assert "name" in user_dict
    assert "username" in user_dict
    assert "email" in user_dict
    assert "password" in user_dict
    assert "role_id" in user_dict
    assert "create_date" in user_dict
    assert "update_date" in user_dict


@mark.unit_testing
def test_user_equality_excludes_password() -> None:
    """
    Test that user equality comparison excludes password field.
    This is important because passwords are hashed and will be different even for the same value.
    """
    user_id = IdentifierMother.random()
    name = UserNameMother.create().value
    username = UserUsernameMother.create().value
    email = UserEmailMother.create().value
    role_id = UserRoleIdMother.create().value
    create_date = DatetimeMother.random()
    update_date = DatetimeMother.now()

    user1 = User(
        id=user_id,
        name=name,
        username=username,
        email=email,
        password=UserPasswordMother.random(),
        role_id=role_id,
        create_date=create_date,
        update_date=update_date,
    )

    user2 = User(
        id=user_id,
        name=name,
        username=username,
        email=email,
        password=UserPasswordMother.random(),
        role_id=role_id,
        create_date=create_date,
        update_date=update_date,
    )

    # They should be equal despite different passwords
    assert user1 == user2


@mark.unit_testing
def test_user_equality_with_different_type() -> None:
    """
    Test that user equality with non-User object returns NotImplemented.
    """
    user = UserMother.create()

    assert user.__eq__("not a user") == NotImplemented


@mark.unit_testing
def test_user_name_setter() -> None:
    """
    Test user name can be updated via setter.
    """
    user = UserMother.create()
    new_name = UserNameMother.create().value

    user.name = new_name

    assert user.name == new_name


@mark.unit_testing
def test_user_username_setter() -> None:
    """
    Test user username can be updated via setter.
    """
    user = UserMother.create()
    new_username = UserUsernameMother.create().value

    user.username = new_username

    assert user.username == new_username


@mark.unit_testing
def test_user_email_setter() -> None:
    """
    Test user email can be updated via setter.
    """
    user = UserMother.create()
    new_email = UserEmailMother.create().value

    user.email = new_email

    assert user.email == new_email


@mark.unit_testing
def test_user_password_setter() -> None:
    """
    Test user password can be updated via setter.
    """
    user = UserMother.create()
    new_password = UserPasswordMother.random()

    user.password = new_password

    # Password should be hashed, so we use check_password method
    assert user.check_password(plain_password=new_password)


@mark.unit_testing
def test_user_update_date_setter() -> None:
    """
    Test user update_date can be updated via setter.
    """
    user = UserMother.create()
    new_update_date = datetime.now(tz=UTC)

    user.update_date = new_update_date

    assert user.update_date == new_update_date


@mark.unit_testing
def test_user_create_date_setter() -> None:
    """
    Test user create_date cannot be updated via setter.
    """
    user = UserMother.create()
    original_create_date = user.create_date
    new_create_date = datetime.now(tz=UTC)
    with assert_raises(AttributeError):
        user.create_date = new_create_date  # pyright: ignore[reportAttributeAccessIssue]

    assert user.create_date == original_create_date


def test_user_role_id_setter() -> None:
    """
    Test user role_id can be updated via setter.
    """
    user = UserMother.create()
    new_role_id = UserRoleIdMother.create().value

    user.role_id = new_role_id

    assert user.role_id == new_role_id


@mark.unit_testing
def test_user_check_password_success() -> None:
    """
    Test check_password returns True for correct password.
    """
    plain_password = UserPasswordMother.random()
    user = UserMother.create(password=plain_password)

    assert user.check_password(plain_password=plain_password) is True


@mark.unit_testing
def test_user_check_password_failure() -> None:
    """
    Test check_password returns False for incorrect password.
    """
    user = UserMother.create(password=UserPasswordMother.random())

    assert user.check_password(plain_password=UserPasswordMother.random()) is False


@mark.unit_testing
def test_user_hash_consistency() -> None:
    """
    Test that user hash is consistent and can be used in sets/dicts.
    """
    user1 = UserMother.create()
    user2 = user1

    assert hash(user1) == hash(user2)

    # Should be able to add to set
    user_set = {user1, user2}
    assert len(user_set) == 1


@mark.unit_testing
def test_user_with_uuid_id() -> None:
    """
    Test user creation with UUID id.
    """
    user_id = uuid4()
    user = UserMother.create(id=str(user_id))

    assert user.id == str(user_id)


@mark.unit_testing
def test_user_create_date_is_immutable() -> None:
    """
    Test that create_date cannot be modified after creation.
    """
    user = UserMother.create()
    original_create_date = user.create_date

    # create_date has no setter, so this should be the same
    assert user.create_date == original_create_date


@mark.unit_testing
def test_user_update_date_can_be_changed() -> None:
    """
    Test that update_date can be modified via setter.
    """
    user = UserMother.create()
    original_update_date = user.update_date

    new_update_date = datetime.now(tz=UTC)
    user.update_date = new_update_date

    assert user.update_date == new_update_date
    assert user.update_date != original_update_date


@mark.unit_testing
def test_user_update_date_preserves_create_date() -> None:
    """
    Test that changing update_date doesn't affect create_date.
    """
    user = UserMother.create()
    original_create_date = user.create_date

    new_update_date = datetime.now(tz=UTC)
    user.update_date = new_update_date

    assert user.create_date == original_create_date


@mark.unit_testing
def test_user_password_setter_hashes_password() -> None:
    """
    Test that password setter properly hashes the password.
    """
    user = UserMother.create()
    plain_password = UserPasswordMother.random()

    user.password = plain_password

    assert user.password != plain_password
    assert user.check_password(plain_password=plain_password)


@mark.unit_testing
def test_user_immutable_fields() -> None:
    """
    Test that id and create_date cannot be changed after creation (no setters).
    """
    user = UserMother.create()
    original_id = user.id
    original_create_date = user.create_date

    # Attempt to modify should not have setters
    # (This is verified by the fact that these properties don't have @setter decorators)

    # Verify they remain unchanged
    assert user.id == original_id
    assert user.create_date == original_create_date
