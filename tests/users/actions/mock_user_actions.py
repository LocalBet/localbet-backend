"""
MockUserActions module.
"""

from typing import Any
from typing_extensions import override
from unittest.mock import Mock

from backend.shared.models import Condition, DataModel
from backend.users.actions import UserActions
from backend.users.errors import UserAlreadyExistsError, UserNotFoundError
from backend.users.models import User


class MockUserActions(UserActions):
    """
    MockUserActions class.
    """

    __search_mock: Mock
    __match_mock: Mock
    __save_mock: Mock
    __update_mock: Mock
    __delete_mock: Mock
    __user: User | None
    __users: list[User]

    def __init__(self) -> None:
        """
        MockUserActions constructor.
        """
        self.__search_mock = Mock()
        self.__save_mock = Mock()
        self.__update_mock = Mock()
        self.__delete_mock = Mock()

    @override
    def search(self, conditions: list[Condition[DataModel]]) -> list[User]:
        """
        Search a single user in the repository using the given conditions.

        Args:
            conditions: Conditions to search for.

        Returns:
            list[User]: List of users that match the conditions.
        """
        self.__search_mock(conditions=conditions)
        return [self.__user] if self.__user else []

    def assert_search_method_called(self, conditions: list[Condition[DataModel]] | None = None) -> None:
        """
        Assert that the search method was called once with the given conditions.

        Args:
            conditions (list[Condition[DataModel]] | None): Conditions to assert.
        """
        if conditions is None:
            self.__search_mock.assert_called_once()
        else:
            self.__search_mock.assert_called_once_with(conditions=conditions)

    def assert_search_method_not_called(self) -> None:
        """
        Assert that the search method was not called.
        """
        self.__search_mock.assert_not_called()

    def prepare_return_search(self, user: User | None) -> None:
        """
        Prepare the search method to return the given user.

        Args:
            user (User | None): User to assert.
        """
        self.__user = user

    @override
    def save(self, user: User) -> None:
        """
        Save user to the repository.

        Args:
            user: User to save.
        """
        self.__save_mock(user=user)

    def assert_save_method_called(self, user: User) -> None:
        """
        Assert that the save method was called once with the given user.

        Args:
            user (User): User to assert.
        """
        self.__save_mock.assert_called_once_with(user=user)

    def assert_save_method_not_called(self) -> None:
        """
        Assert that the save method was not called.
        """
        self.__save_mock.assert_not_called()

    def prepare_user_already_exists_when_saving(self, field: str, value: Any) -> None:
        """
        Prepare the save method to raise a UserAlreadyExistsError when attempting to save a user with the given field
        and value.

        Args:
            field (str): Field of the user that caused the conflict.
            value (Any): Value of the field that caused the conflict.
        """
        self.__save_mock.side_effect = UserAlreadyExistsError(field=field, value=value)

    @override
    def update(self, user: User) -> None:
        """
        Update user in the repository.

        Args:
            user (User): User to be updated.

        Raises:
            UserNotFoundError: If user is not found.
            UserAlreadyExistsError: If user already exists.
        """
        self.__update_mock(user=user)

    def assert_update_method_called(self, user: User) -> None:
        """
        Assert that the update method was called once with the given user.

        Args:
            user (User): User to assert.
        """
        self.__update_mock.assert_called_once_with(user=user)

    def assert_update_method_not_called(self) -> None:
        """
        Assert that the update method was not called.
        """
        self.__update_mock.assert_not_called()

    @override
    def delete(self, user: User) -> None:
        """
        Delete user from the repository.

        Args:
            user: User to delete.
        """
        self.__delete_mock(user=user)

    def assert_delete_method_called(self, user: User) -> None:
        """
        Assert that the delete method was called once with the given user.

        Args:
            user (User): User to assert.
        """
        self.__delete_mock.assert_called_once_with(user=user)

    def assert_delete_method_not_called(self) -> None:
        """
        Assert that the delete method was not called.
        """
        self.__delete_mock.assert_not_called()

    def prepare_user_not_found_when_deleting(self, user: User) -> None:
        """
        Prepare the delete method to raise a UserNotFoundError when attempting to delete the given user.

        Args:
            user (User): User to assert.
        """
        self.__delete_mock.side_effect = UserNotFoundError(field="id", value=user.id)
