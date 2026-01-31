"""
GroupRoleTypeName value object.
"""

from typing_extensions import override
from backend.shared.models import ValueObject
from backend.group_roles_type.errors import GroupRoleTypeNameTypeError, GroupRoleTypeNameMinLengthError, GroupRoleTypeNameMaxLengthError, GroupRoleTypeNameContainsInvalidCharactersError

class GroupRoleTypeName(ValueObject[str]):
    """
    GroupRoleTypeName value object.
    """

    __ROLE_NAME_MIN_LENGTH: int = 3
    __ROLE_NAME_MAX_LENGTH: int = 32

    @override
    def _validate(self, value: str) -> None:
        """
        This method validates that the value follows the domain rules.

        Args:
            value (str): GroupRoleType name.

        Raises:
            GroupRoleTypeNameTypeError: If the value is not a string.
            GroupRoleTypeNameMinLengthError: If the value length is less than the minimum allowed.
            GroupRoleTypeNameMaxLengthError: If the value length is greater than the maximum allowed.
            GroupRoleTypeNameContainsInvalidCharactersError: If the value contains invalid characters.
            GroupRoleTypeNameContainsInvalidCharactersError: If the value contains leading or trailing whitespaces.
        """
        if type(value) is not str:
            raise GroupRoleTypeNameTypeError(name=value)

        if len(value) < self.__ROLE_NAME_MIN_LENGTH:
            raise GroupRoleTypeNameMinLengthError(name=value, min_length=self.__ROLE_NAME_MIN_LENGTH)

        if len(value) > self.__ROLE_NAME_MAX_LENGTH:
            raise GroupRoleTypeNameMaxLengthError(name=value, max_length=self.__ROLE_NAME_MAX_LENGTH)

        if not value.isprintable():
            raise GroupRoleTypeNameContainsInvalidCharactersError(name=value)

        if value != value.strip():
            raise GroupRoleTypeNameContainsInvalidCharactersError(name=value)
