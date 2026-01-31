"""
Permission domain model.
"""

from datetime import datetime

from backend.shared.models import DataModel
from .permission_id import PermissionId
from .permission_action import PermissionAction
from .permission_scope import PermissionScope
from .permission_create_date import PermissionCreatedDate
from .permission_update_date import PermissionUpdateDate
from .permission_resource import PermissionResource
from .permission_resouce_type import PermissionResourceType
from .permission_action_type import PermissionActionType
from .permission_scope_type import PermissionScopeType
from backend.shared.models import ID
from uuid import UUID

class Permission(DataModel):
    """Simple Permission domain model."""

    __id: ID
    __scope: PermissionScope
    __action: PermissionAction
    __resource: PermissionResource
    __create_date: PermissionCreatedDate
    __update_date: PermissionUpdateDate

    def __init__(
        self,
        id: str | UUID,
        scope: PermissionScopeType,
        action: PermissionActionType,
        resource: PermissionResourceType,
        create_date: datetime,
        update_date: datetime,
    ) -> None:
        """
        Permission domain model constructor.
        """
        self.__id = PermissionId(value=id)
        self.__scope = PermissionScope(value=scope)
        self.__action = PermissionAction(value=action)
        self.__resource = PermissionResource(value=resource)
        self.__create_date = PermissionCreatedDate(value=create_date)
        self.__update_date = PermissionUpdateDate(value=update_date)

    @property
    def id(self) -> str:
        return self.__id.value

    @property
    def scope(self) -> str:
        return self.__scope.value

    @property
    def action(self) -> str:
        return self.__action.value

    @property
    def resource(self) -> str:
        return self.__resource.value

    @property
    def create_date(self) -> datetime:
        return self.__create_date.value

    @property
    def update_date(self) -> datetime:
        return self.__update_date.value
